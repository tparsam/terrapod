# /// script
# requires-python = ">=3.10,<3.12"
# dependencies = ["numpy", "scipy", "matplotlib", "pymoo>=0.6", "mujoco<3.3"]
# ///
"""Genetic search v2: lobed ring with a rounded rim, scored with 3D landings.

What changed from pod_ga.py (v1), and why:
  * 8th gene `rim`: rounded outer rim (0 to 3.5 mm). v1's pick 1 rested on its edge in 25% of 3D landings.
  * Rolling objective = median travel over the same random 3D landings for every design (MuJoCo),
    instead of v1's 2D edge-roll model.
  * New rules: rests on its edge in at most --edge-max % of landings; rings cannot hook together
    (hole narrower than the ring's thickness and wall); scenario B also needs the narrowest
    width >= 25 mm (strict reading of "2.5-3 cm diameter").
  * The final picks are re-scored with 200 landings and the fine-mesh FEM, next to today's lead.

Run:  uv run --python 3.11 geometry/ga2.py            (both scenarios; ~20 min on 10 cores)
"""
import argparse
import csv
import dataclasses
import math
import sys
from pathlib import Path

import numpy as np

import moulds
import pod_ga as pg
import waves3d as w3

BOUNDS2 = {**pg.BOUNDS, "rim": (0.0, 3.5)}
LEAD = pg.Pod(25.02, 6, 7.69, 0.2, 4, 2.98, 0.96, rim=2.5)  # current lead: v1 pick 1 + 2.5 mm rounded rim
SCENARIOS = {"A_tip_to_tip": 0.0, "B_narrowest_25mm": 25.0}  # minimum narrowest width (mm)


def narrowest_width_mm(pod, n=1440):
    """Smallest caliper width of the outline (mm): what a ruler across the pod's narrowest way reads."""
    th = np.arange(n) * 2 * np.pi / n
    r = pg.r_out(pod, th) * 1000
    pts = np.stack([r * np.cos(th), r * np.sin(th)], 1)
    u = np.stack([np.cos(th[: n // 2]), np.sin(th[: n // 2])], 1)
    proj = pts @ u.T
    return float((proj.max(0) - proj.min(0)).min())


def wall_mm(pod):
    th = np.arange(720) * 2 * np.pi / 720
    return pg.r_out(pod, th).min() * 1000 - pod.hole / 2


def hooks_into_hole(pod):
    """True if one ring's band could pass through another's hole (rings chain in a hopper)."""
    return pod.hole >= min(pod.t_edge, wall_mm(pod))


def to_pod(x):
    return pg.Pod(D=x[0], hole=x[1], t_edge=x[2], dome=x[3], n=int(round(x[4])), a=x[5], p=x[6], rim=x[7])


def travel_and_edge(runs, t_max, cap_m):
    """Travel (cm) per landing, with any pod still moving at t_max counted as rolled away (cap_m),
    and the % of landings that came to rest standing on edge."""
    d = np.array([cap_m if r["t_s"] >= t_max - 1e-9 else r["dist_m"] for r in runs]) * 100
    d = np.maximum(d, np.array([r["dist_m"] for r in runs]) * 100)
    edge = 100 * np.mean([(not r["flat"]) and r["t_s"] < t_max - 1e-9 for r in runs])
    return d, float(edge)


def landings_3d(pod, q, v, w, mesh=(180, 12), fast=True):
    """(median cm, 90th percentile cm, % resting on edge). fast (search): stop at 1 m or 2 s and count
    a pod still moving at 2 s as rolled away (1 m). Otherwise (final check): full 4 s, no cap."""
    V, F = pg.surface_mesh(pod, *mesh)
    model = w3.build(V, F)
    t_max, cap = (2.0, 1.0) if fast else (4.0, math.inf)
    res = [w3.throw(V, F, quat=q[i], v=v[i], w=w[i], model=model, t_max=t_max, max_dist=cap) for i in range(len(q))]
    d, edge = travel_and_edge(res, t_max, cap if fast else 0.0)
    return float(np.median(d)), float(np.percentile(d, 90)), edge


def score(pod, cfg, min_width, q, v, w, final=False):
    """All metrics for one design. final=True: fine-mesh FEM (the landings passed in decide the 3D part)."""
    m = pg.evaluate(pod, cfg, full=final)
    m["travel_median_cm"], m["travel_p90_cm"], m["on_edge_pct"] = landings_3d(pod, q, v, w, fast=not final)
    m["narrowest_width_mm"] = narrowest_width_mm(pod)
    m["hooks"] = hooks_into_hole(pod)
    G = pg.constraints(m, cfg) + [m["on_edge_pct"] - cfg.edge_max,
                                  pod.hole - min(pod.t_edge, m["wall_mm"]) + 1e-6,
                                  min_width - m["narrowest_width_mm"]]
    return m, G


def _eval_job(args):
    x, cfg, min_width, q, v, w = args
    m, G = score(to_pod(x), cfg, min_width, q, v, w)
    return [m["mass_g"], m["travel_median_cm"], m["stress_rel"]], G


def run_scenario(name, min_width, cfg, pool):
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import Problem
    from pymoo.optimize import minimize

    q, v, w = w3.random_landings(cfg.landings, seed=11)  # search set; the final check uses a different one
    lo = np.array([b[0] for b in BOUNDS2.values()], float)
    hi = np.array([b[1] for b in BOUNDS2.values()], float)
    hi[4] += 0.49

    class P(Problem):
        def __init__(self):
            super().__init__(n_var=len(BOUNDS2), n_obj=3, n_ieq_constr=7, xl=lo, xu=hi)

        def _evaluate(self, X, out, *args, **kwargs):
            jobs = [(x, cfg, min_width, q, v, w) for x in X]
            res = list(pool.imap(_eval_job, jobs, chunksize=1)) if pool else list(map(_eval_job, jobs))
            out["F"] = np.array([r[0] for r in res])
            out["G"] = np.array([r[1] for r in res])

    res = minimize(P(), NSGA2(pop_size=cfg.pop), ("n_gen", cfg.gens), seed=cfg.seed, verbose=False)
    feasible = res.X is not None
    X = np.atleast_2d(res.X) if feasible else res.pop.get("X")[np.argsort(res.pop.get("CV")[:, 0])][: cfg.picks]
    pods = list({dataclasses.astuple(p): p for p in map(to_pod, X)}.values())

    qf, vf, wf = w3.random_landings(cfg.final_landings, seed=7)  # same 200 landings as waves3d.py
    jobs = [(p, cfg, min_width, qf, vf, wf, True) for p in [LEAD, *pods]]
    scored = pool.starmap(score, jobs) if pool else [score(*j) for j in jobs]
    lead_m, metrics = scored[0][0], [s[0] for s in scored[1:]]
    ok = [all(g <= 0 for g in s[1]) for s in scored[1:]]
    F = np.array([[m["mass_g"], m["travel_median_cm"], m["stress_rel"]] for m in metrics])
    picks = pg.pick_spread(F, cfg.picks)
    return pods, metrics, ok, F, picks, lead_m, scored[0][1], feasible


def write_outputs(out, name, min_width, cfg, pods, metrics, ok, F, picks, lead_m, lead_G, feasible):
    out.mkdir(parents=True, exist_ok=True)
    keys = list(dataclasses.asdict(LEAD))
    mcols = ["mass_g", "cost_aed_material", "travel_median_cm", "travel_p90_cm", "on_edge_pct", "stress_rel",
             "cover_mm", "wall_mm", "narrowest_width_mm", "max_thick_mm", "tip_barrier_mm", "sa_per_vol_1_per_mm"]
    with open(out / "pareto.csv", "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["pick", "meets_all_rules", *keys, *mcols])
        for i, (p, m) in enumerate(zip(pods, metrics)):
            wr.writerow([picks.index(i) + 1 if i in picks else "", ok[i], *dataclasses.astuple(p),
                         *(round(float(m[c]), 4) for c in mcols)])
    for k, i in enumerate(picks, 1):
        pg.write_stl(out / f"pick_{k}.stl", *pg.surface_mesh(pods[i], n_theta=720, n_s=48))
        pg.write_stl(out / f"pick_{k}_mould_half.stl", *moulds.mould_half(pods[i])[:2])

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    lead_F = [lead_m["mass_g"], lead_m["travel_median_cm"], lead_m["stress_rel"]]
    for k, (j, label) in enumerate([(1, "median travel after landing (cm, 3D)"), (2, "impact stress vs plain ring")]):
        sc = ax[k].scatter(F[:, 0], F[:, j], c=F[:, 3 - j], cmap="viridis", s=18)
        ax[k].scatter(F[picks, 0], F[picks, j], facecolors="none", edgecolors="crimson", s=110, lw=1.5)
        ax[k].scatter([lead_F[0]], [lead_F[j]], marker="*", s=180, c="black", label="current lead")
        for r, i in enumerate(picks, 1):
            ax[k].annotate(str(r), (F[i, 0], F[i, j]), xytext=(5, 5), textcoords="offset points", color="crimson")
        ax[k].set_xlabel("mass per pod (g)")
        ax[k].set_ylabel(label)
        ax[k].legend(loc="upper right", fontsize=8)
        fig.colorbar(sc, ax=ax[k], label="impact stress vs plain ring" if j == 1 else "median travel (cm)")
    fig.suptitle(f"GA v2, scenario {name}: picks circled, current lead = star")
    fig.tight_layout()
    fig.savefig(out / "pareto.png", dpi=150)
    plt.close(fig)

    cols = ["mass_g", "travel_median_cm", "travel_p90_cm", "on_edge_pct", "stress_rel", "cover_mm",
            "narrowest_width_mm", "max_thick_mm"]
    fmt = lambda v: f"{v:g}" if isinstance(v, int) else f"{v:.2f}"
    lines = [f"# GA v2, scenario {name}", "",
             f"NSGA-II, population {cfg.pop}, {cfg.gens} generations, {cfg.landings} search landings per design. "
             f"Picks and the current lead re-scored on {cfg.final_landings} landings (the waves3d.py set) with the "
             "fine-mesh FEM.", "",
             ("**No design met every rule in this scenario; the rows below are the closest misses.**" if not feasible
              else f"{len(pods)} designs on the trade-off front."), "",
             f"Rules: Calligonum pocket >= {cfg.cover_min} mm, wall >= {cfg.wall_min} mm, lobe tip radius >= "
             f"{cfg.tip_r_min} mm, valley radius >= {cfg.valley_r_min} mm, rests on edge <= {cfg.edge_max}% of landings, "
             "hole narrower than the ring's thickness and wall (no hooking)"
             + (f", narrowest width >= {min_width:g} mm" if min_width else "") + ". "
             f"Density {cfg.density} g/cm³ (placeholder).", "",
             "| design | meets rules | " + " | ".join(keys) + " | " + " | ".join(cols) + " |",
             "|---" * (2 + len(keys) + len(cols)) + "|"]
    lead_ok = all(g <= 0 for g in lead_G)
    lines.append("| **current lead** | " + ("yes" if lead_ok else "**no**") + " | "
                 + " | ".join(fmt(v) for v in dataclasses.astuple(LEAD)) + " | "
                 + " | ".join(f"{lead_m[c]:.2f}" for c in cols) + " |")
    for k, i in enumerate(picks, 1):
        lines.append(f"| pick {k} | {'yes' if ok[i] else 'no'} | "
                     + " | ".join(fmt(v) for v in dataclasses.astuple(pods[i])) + " | "
                     + " | ".join(f"{metrics[i][c]:.2f}" for c in cols) + " |")
    lines += ["", "Files: `pick_N.stl` (pod), `pick_N_mould_half.stl` (press mould, print twice), `pareto.csv`, "
              "`pareto.png`."]
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pop", type=int, default=60)
    ap.add_argument("--gens", type=int, default=40)
    ap.add_argument("--landings", type=int, default=60, help="3D landings per design during the search")
    ap.add_argument("--final-landings", type=int, default=200)
    ap.add_argument("--picks", type=int, default=4)
    ap.add_argument("--edge-max", type=float, default=5.0, help="max %% of landings resting on edge")
    ap.add_argument("--scenarios", default=",".join(SCENARIOS))
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--density", type=float, default=1.2)
    ap.add_argument("--cost-per-kg", type=float, default=3.0)
    ap.add_argument("--cover-min", type=float, default=4.0)
    ap.add_argument("--wall-min", type=float, default=4.0)
    ap.add_argument("--tip-r-min", type=float, default=1.0)
    ap.add_argument("--valley-r-min", type=float, default=0.5)
    ap.add_argument("--out", default="geometry/out/ga2")
    cfg = ap.parse_args(sys.argv[1:] if argv is None else argv)
    cfg.v0, cfg.cap = 1.0, 2.0  # for pod_ga.evaluate's 2D roll (reported only)

    from multiprocessing import get_context
    pool = get_context("spawn").Pool(cfg.workers) if cfg.workers > 1 else None
    try:
        for name in cfg.scenarios.split(","):
            min_width = SCENARIOS[name]
            result = run_scenario(name, min_width, cfg, pool)
            write_outputs(Path(cfg.out) / name, name, min_width, cfg, *result)
    finally:
        if pool:
            pool.close()


if __name__ == "__main__":
    main()
