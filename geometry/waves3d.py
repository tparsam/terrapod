# /// script
# requires-python = ">=3.10,<3.12"
# dependencies = ["numpy", "scipy", "matplotlib", "pymoo>=0.6", "mujoco<3.3"]
# ///
"""Do up-and-down (pie-crust) rim waves help? 3D rigid-body test in MuJoCo.

Every design gets the same randomised landings (paired comparison): random orientation, a
sideways and downward speed, and a spin, starting just above flat hard ground. We record how far
each pod travels before it stops and whether it ends lying flat.

Run:  uv run geometry/waves3d.py            (about 5 minutes; writes geometry/out/waves/)
ponytail: hard flat ground, rigid pod, Coulomb friction 0.6, no rolling resistance, no sand.
It ranks shapes; the ramp and fan tests in TEST_PROTOCOL.md give the real numbers.
"""
import csv
import math
import sys
from pathlib import Path

import mujoco
import numpy as np

import moulds
import pod_ga as pg

DENSITY = 1200.0  # kg/m^3, placeholder as in pod_ga


def wavy_mesh(pod, m, b, n_theta=240, n_s=24):
    """pod_ga.surface_mesh (including any rounded rim, pod.rim) with the rim rippled up and down by
    pod_ga.wave_lift (m waves, b mm)."""
    V, F = pg.surface_mesh(pod, n_theta=n_theta, n_s=n_s)
    if m and b:
        th = np.arctan2(V[:, 1], V[:, 0])
        ri = pod.hole / 2000
        s = np.clip((np.hypot(V[:, 0], V[:, 1]) - ri) / (pg.r_out(pod, th) - ri), 0, 1)
        V = V.copy()
        V[:, 2] += pg.wave_lift(th, s, m, b)
    return V, F


def build(V, F):
    xml = f"""<mujoco>
  <option timestep="0.0002"/>
  <default><geom friction="0.6 0.005 0.0001" condim="3" solref="0.002 1"/></default>
  <asset><mesh name="pod" inertia="exact" vertex="{' '.join(map(str, V.ravel()))}"
               face="{' '.join(map(str, F.ravel()))}"/></asset>
  <worldbody>
    <geom type="plane" size="20 20 0.1"/>
    <body name="pod"><freejoint/><geom type="mesh" mesh="pod" density="{DENSITY}"/></body>
  </worldbody>
</mujoco>"""
    return mujoco.MjModel.from_xml_string(xml)


def _sym_axis_local(model):
    """The ring's symmetry axis in the pod's body frame: the direction its vertices are thinnest in.
    (MuJoCo re-orients meshes to its own principal frame, so we measure rather than assume.)"""
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    pts = data.geom_xpos[1] + model.mesh_vert @ data.geom_xmat[1].reshape(3, 3).T - data.xpos[1]
    return np.linalg.eigh(np.cov(pts.T))[1][:, 0]


def _quat_between(a, t):
    """Unit quaternion (w, x, y, z) rotating unit vector a onto t."""
    t = np.asarray(t, float) / np.linalg.norm(t)
    v, c = np.cross(a, t), float(a @ t)
    if np.linalg.norm(v) < 1e-12:
        if c > 0:
            return np.array([1.0, 0, 0, 0])
        perp = np.cross(a, [1, 0, 0] if abs(a[0]) < 0.9 else [0, 1, 0])
        return np.array([0.0, *(perp / np.linalg.norm(perp))])
    q = np.array([1 + c, *v])
    return q / np.linalg.norm(q)


def throw(V, F, pos_tilt=0.0, v=(0, 0, 0), w=(0, 0, 0), quat=None, model=None, t_max=4.0, max_dist=math.inf):
    """One landing. pos_tilt tilts the symmetry axis from vertical towards -y (pi/2 = upright wheel
    rolling along x). v and w are world-frame linear and angular velocity. Stops early once the pod is
    max_dist (m) from where it landed: it has clearly rolled away, and the rest only costs time.
    Returns {"dist_m": horizontal travel, "flat": ends lying flat, "t_s": time}."""
    model = model or build(V, F)
    sym = _sym_axis_local(model)
    data = mujoco.MjData(model)
    data.qpos[3:7] = quat if quat is not None else _quat_between(sym, (0, -np.sin(pos_tilt), np.cos(pos_tilt)))
    data.qpos[2] = 0.1
    mujoco.mj_forward(model, data)
    verts = data.geom_xpos[1] + model.mesh_vert @ data.geom_xmat[1].reshape(3, 3).T
    data.qpos[2] -= verts[:, 2].min() - 0.001  # lowest point 1 mm above the ground
    R = data.xmat[1].reshape(3, 3)
    data.qvel[:3], data.qvel[3:] = v, R.T @ np.asarray(w, float)  # free joint: angular velocity is body-frame
    mujoco.mj_forward(model, data)
    start, still = data.qpos[:2].copy(), 0
    cos_flat = np.cos(np.radians(25))
    while data.time < t_max and still < 3 and np.linalg.norm(data.qpos[:2] - start) < max_dist:
        mujoco.mj_step(model, data, nstep=100)
        lying_flat = abs((data.xmat[1].reshape(3, 3) @ sym)[2]) > cos_flat
        at_rest = np.linalg.norm(data.qvel[:3]) < 0.003 and np.linalg.norm(data.qvel[3:]) < 0.3
        # a pod lying flat and barely sliding is settled even if it still spins in place
        settled = at_rest or (lying_flat and np.linalg.norm(data.qvel[:2]) < 0.01 and abs(data.qvel[2]) < 0.01)
        still = still + 1 if settled else 0
    axis = data.xmat[1].reshape(3, 3) @ sym
    return {"dist_m": float(np.linalg.norm(data.qpos[:2] - start)), "flat": bool(abs(axis[2]) > np.cos(np.radians(25))),
            "t_s": float(data.time)}


def _closed_vol(V, F):
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    return np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6


def random_landings(n, seed=7):
    """Paired initial conditions: orientation, sideways 0.5-2 m/s, downward 0.5-2 m/s, spin 0-30 rad/s."""
    rng = np.random.default_rng(seed)
    q = rng.normal(size=(n, 4))
    q /= np.linalg.norm(q, axis=1, keepdims=True)
    head = rng.uniform(0, 2 * np.pi, n)
    vh = rng.uniform(0.5, 2.0, n)
    v = np.stack([vh * np.cos(head), vh * np.sin(head), -rng.uniform(0.5, 2.0, n)], 1)
    wdir = rng.normal(size=(n, 3))
    w = wdir / np.linalg.norm(wdir, axis=1, keepdims=True) * rng.uniform(0, 30, (n, 1))
    return q, v, w


SMOOTH = pg.Pod(25.02, 6, 7.69, 0.2, 0, 0, 1)
P1 = pg.Pod(25.02, 6, 7.69, 0.2, 4, 2.98, 0.96)  # pick 1
P1R = pg.Pod(25.02, 6, 7.69, 0.2, 4, 2.98, 0.96, rim=2.5)  # pick 1 with a 2.5 mm rounded rim
TEETH = pg.Pod(25, 6, 7.7, 0.2, 16, 1.5, 1)       # in-plane pie-crust teeth
VARIANTS = {  # name: (pod, waves m, amplitude b mm)
    "pick 1 (4 lobes), no waves": (P1, 0, 0.0),
    "pick 1 + 4 waves x 1.5 mm": (P1, 4, 1.5),
    "pick 1 + 8 waves x 0.75 mm": (P1, 8, 0.75),
    "pick 1 + 8 waves x 1.5 mm": (P1, 8, 1.5),
    "pick 1 + 12 waves x 1.0 mm": (P1, 12, 1.0),
    "smooth ring, no waves": (SMOOTH, 0, 0.0),
    "smooth ring + 8 waves x 1.5 mm (pie crust)": (SMOOTH, 8, 1.5),
    "16 in-plane teeth x 1.5 mm": (TEETH, 0, 0.0),
    "pick 1, rounded rim 2.5 mm": (P1R, 0, 0.0),
    "pick 1, rounded rim 2.5 mm + 8 waves x 0.75 mm": (P1R, 8, 0.75),
}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    n = int(argv[0]) if argv else 150
    out = Path(argv[1] if len(argv) > 1 else "geometry/out/waves")
    out.mkdir(parents=True, exist_ok=True)
    q, v, w = random_landings(n)
    res = {}
    for name, (pod, m, b) in VARIANTS.items():
        V, F = wavy_mesh(pod, m, b, n_theta=180, n_s=12)
        model = build(V, F)
        res[name] = [throw(V, F, quat=q[i], v=v[i], w=w[i], model=model) for i in range(n)]
        print(f"{name}: median {np.median([r['dist_m'] for r in res[name]]) * 100:.1f} cm", flush=True)

    lead = np.array([r["dist_m"] for r in res["pick 1 (4 lobes), no waves"]])
    rows = []
    for name, (pod, m, b) in VARIANTS.items():
        V, F = wavy_mesh(pod, m, b)
        d = np.array([r["dist_m"] for r in res[name]])
        rows.append({"design": name, "median_cm": np.median(d) * 100, "p90_cm": np.percentile(d, 90) * 100,
                     "mean_cm": d.mean() * 100, "ends_flat_pct": 100 * np.mean([r["flat"] for r in res[name]]),
                     "beats_pick1_pct": 100 * np.mean(d < lead - 1e-3),
                     "ends_on_edge_pct": 100 * np.mean([(not r["flat"]) and r["t_s"] < 3.99 for r in res[name]]),
                     "mass_g": _closed_vol(V, F) * DENSITY * 1000, "face_gap_mm": 2 * b})
    with open(out / "results.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.boxplot([np.array([r["dist_m"] for r in res[k]]) * 100 for k in VARIANTS], orientation="horizontal",
               tick_labels=list(VARIANTS), showfliers=False)
    ax.set_xlabel("distance travelled after landing (cm), hard flat ground")
    ax.invert_yaxis()
    ax.set_title(f"{n} identical random landings per design (MuJoCo 3D rigid-body)")
    fig.tight_layout()
    fig.savefig(out / "distances.png", dpi=140)
    plt.close(fig)

    lines = ["# Up-and-down rim waves: 3D landing test", "",
             f"{n} identical random landings per design: random orientation, sideways 0.5 to 2 m/s, downward "
             "0.5 to 2 m/s, spin 0 to 30 rad/s, starting 1 mm above hard flat ground (friction 0.6). MuJoCo "
             f"{mujoco.__version__}, rigid pod, density {DENSITY / 1000:g} g/cm³. Ranks shapes only: sand stops "
             "every pod sooner.", "",
             "`beats_pick1_pct`: share of the same landings where this design travelled less than pick 1. "
             "`face_gap_mm`: gap between a flat face and the ground at the rim when the pod lies on its wave "
             "crests (seeds on that face lose soil contact).", "",
             "`ends_on_edge`: share of landings where the pod came to rest standing on its edge (no seeded face on the "
             "ground).", "",
             "| design | median (cm) | 90th pct (cm) | mean (cm) | ends flat | ends on edge | beats pick 1 | mass (g) | face gap (mm) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['design']} | {r['median_cm']:.1f} | {r['p90_cm']:.1f} | {r['mean_cm']:.1f} | "
                     f"{r['ends_flat_pct']:.0f}% | {r['ends_on_edge_pct']:.0f}% | {r['beats_pick1_pct']:.0f}% | {r['mass_g']:.2f} | {r['face_gap_mm']:.1f} |")

    best = min((r for r in rows if r["face_gap_mm"] > 0 and r["design"].startswith("pick 1")
                and "rounded" not in r["design"]), key=lambda r: r["median_cm"])
    pod, m, b = VARIANTS[best["design"]]
    tag = f"pick_1_waves_{m}x{b:g}mm"
    for side, part in ((1, "top"), (-1, "bottom")):
        pg.write_stl(out / f"{tag}_{part}_mould_half.stl", *moulds.mould_half(pod, wave=(m, b), side=side)[:2])
    pg.write_stl(out / f"{tag}.stl", *wavy_mesh(pod, m, b, n_theta=720, n_s=48))
    lines += ["", f"Moulds written for the best wavy variant ({best['design']}): `{tag}_top_mould_half.stl` and "
              f"`{tag}_bottom_mould_half.stl` (print one of each; the bottom half flips onto the top). Pod: `{tag}.stl`."]
    (out / "results.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
