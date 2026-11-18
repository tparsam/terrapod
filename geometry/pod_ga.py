# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib", "pymoo>=0.6"]
# ///
"""Multi-objective genetic search (NSGA-II) for the crimped-ring TerraPod.

Objectives (all minimised):
  mass_g      material per pod: drives cost, pods per flight, impact force
  roll_m      distance a pod rolls on its edge after landing (rimless-wheel model)
  stress_rel  peak tensile stress for an edge-on impact, vs a plain 30/10 x 10 mm ring (2D FEM)

Run:  uv run geometry/pod_ga.py --out geometry/out
Read geometry/README.md for what the models do and do not cover.
"""
import argparse
import csv
import math
from dataclasses import asdict, dataclass, replace
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.spatial import ConvexHull

G = 9.81

# name: (low, high) in mm, except n (count) and p (shape exponent)
BOUNDS = {
    "D": (25.0, 30.0),      # tip-to-tip outer diameter (brief: 2.5 to 3 cm)
    "hole": (6.0, 14.0),    # centre hole diameter
    "t_edge": (4.0, 12.0),  # thickness at the inner and outer walls
    "dome": (0.0, 3.0),     # extra bulge of each face at mid-width
    "n": (3, 24),           # number of crimp lobes
    "a": (0.0, 3.0),        # crimp depth (0 = smooth ring)
    "p": (0.5, 3.0),        # crimp shape: <1 broad valleys and pointed lobes, >1 broad lobes and narrow valleys
}


@dataclass(frozen=True)
class Pod:
    D: float
    hole: float
    t_edge: float
    dome: float
    n: int
    a: float
    p: float
    rim: float = 0.0  # rounded outer rim width, mm (0 = square edge); see rim_taper


# ---------- geometry (SI units inside, mm only at the edges) ----------

def r_out(pod, th):
    """Outer radius (m) at angle th. A lobe tip points straight down (th = -pi/2)."""
    if pod.n == 0 or pod.a == 0:
        return np.full_like(th, pod.D / 2000)
    f = ((1 - np.cos(pod.n * (th + np.pi / 2))) / 2) ** pod.p
    return (pod.D / 2 - pod.a * f) / 1000


def half_thick(pod, s):
    """Half thickness (m) at normalised radial position s (0 = hole wall, 1 = outer wall)."""
    return (pod.t_edge / 2 + pod.dome * np.sin(np.pi * s)) / 1000


def wave_lift(th, s, m, b):
    """Up-and-down (pie-crust) ripple, m: number of waves, b: amplitude in mm at the rim. Returns m.
    Grows linearly from 0 at the hole wall (s = 0) to b at the outer wall (s = 1)."""
    return b / 1000 * s * np.cos(m * th)


def rim_taper(u_mm, round_mm):
    """Thickness factor for a rounded outer rim: 1 more than round_mm in from the outer wall,
    easing (quarter ellipse) to 0.35 at the wall, like a coin's bevelled edge."""
    if not round_mm:
        return np.ones_like(u_mm)
    x = np.clip((round_mm - u_mm) / round_mm, 0, 1)
    return 0.35 + 0.65 * np.sqrt(1 - x**2)


def mass_props(pod, density, n_theta=720, n_s=200):
    """(volume m^3, mass kg, inertia about the ring axis kg m^2), by midpoint quadrature."""
    th = (np.arange(n_theta) + 0.5) * 2 * np.pi / n_theta
    s = (np.arange(n_s) + 0.5) / n_s
    ri = pod.hole / 2000
    ro = r_out(pod, th)[:, None]
    r = ri + (ro - ri) * s
    dV = 2 * half_thick(pod, s) * rim_taper((ro - r) * 1000, pod.rim) * r * (ro - ri) / n_s * (2 * np.pi / n_theta)
    vol = dV.sum()
    return vol, density * vol, density * (r**2 * dV).sum()


def surface_mesh(pod, n_theta=240, n_s=24, n_wall=4):
    """Closed triangle mesh (vertices m, faces) made by sweeping the cross-section loop round the axis."""
    s_up = np.linspace(0, 1, n_s)
    wall = np.linspace(1, -1, n_wall + 1)[1:-1]
    # loop in (s, z-sign*h): top face outwards, outer wall down, bottom face inwards, hole wall up
    loop_s = np.concatenate([s_up, np.ones(len(wall)), s_up[::-1], np.zeros(len(wall))])
    loop_z = np.concatenate([half_thick(pod, s_up), wall * half_thick(pod, 1.0),
                             -half_thick(pod, s_up[::-1]), -wall * half_thick(pod, 0.0)])
    th = np.arange(n_theta) * 2 * np.pi / n_theta
    ri = pod.hole / 2000
    ro = r_out(pod, th)[:, None]
    r = ri + (ro - ri) * loop_s
    z = loop_z * rim_taper((ro - r) * 1000, pod.rim)
    V = np.stack([r * np.cos(th)[:, None], r * np.sin(th)[:, None], z], -1).reshape(-1, 3)
    L = len(loop_s)
    j, l = np.meshgrid(np.arange(n_theta), np.arange(L), indexing="ij")
    a, b = j * L + l, ((j + 1) % n_theta) * L + l
    c, d = ((j + 1) % n_theta) * L + (l + 1) % L, j * L + (l + 1) % L
    F = np.concatenate([np.stack([a, b, c], -1).reshape(-1, 3), np.stack([a, c, d], -1).reshape(-1, 3)])
    p0, p1, p2 = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    if np.einsum("ij,ij->i", p0, np.cross(p1, p2)).sum() < 0:
        F = F[:, ::-1]
    return V, F


def write_stl(path, V, F):
    tri = V[F] * 1000  # mm, the unit slicers assume
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-30
    rec = np.zeros(len(F), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("attr", "<u2")])
    rec["n"], rec["v"] = n, tri
    with open(path, "wb") as fh:
        fh.write(b"TerraPod".ljust(80, b" "))
        fh.write(np.uint32(len(F)).tobytes())
        fh.write(rec.tobytes())


# ---------- 2D plane-stress FEM (edge-on impact) ----------

def plane_mesh(pod, n_theta=360, n_r=8):
    """Triangles over the pod seen from above. Returns nodes (m), tris, thickness per tri (m)."""
    th = np.arange(n_theta) * 2 * np.pi / n_theta
    ri = pod.hole / 2000
    solid = ri == 0
    s = np.linspace(1 / n_r, 1, n_r) if solid else np.linspace(0, 1, n_r + 1)
    k = len(s)
    r = ri + (r_out(pod, th)[:, None] - ri) * s
    nodes = np.stack([r * np.cos(th)[:, None], r * np.sin(th)[:, None]], -1).reshape(-1, 2)
    node_s = np.tile(s, n_theta)
    j, i = np.meshgrid(np.arange(n_theta), np.arange(k - 1), indexing="ij")
    a, b = j * k + i, ((j + 1) % n_theta) * k + i
    tris = np.concatenate([np.stack([a, b, b + 1], -1).reshape(-1, 3),
                           np.stack([a, b + 1, a + 1], -1).reshape(-1, 3)])
    if solid:  # fan to a centre node
        nodes = np.vstack([nodes, [0.0, 0.0]])
        node_s = np.append(node_s, 0.0)
        jj = np.arange(n_theta)
        tris = np.vstack([tris, np.stack([np.full(n_theta, len(nodes) - 1), jj * k, ((jj + 1) % n_theta) * k], -1)])
    x, y = nodes[tris, 0], nodes[tris, 1]
    flip = (x[:, 1] - x[:, 0]) * (y[:, 2] - y[:, 0]) - (x[:, 2] - x[:, 0]) * (y[:, 1] - y[:, 0]) < 0
    tris[flip] = tris[flip][:, ::-1]
    c = nodes[tris].mean(axis=1)
    u = r_out(pod, np.arctan2(c[:, 1], c[:, 0])) - np.hypot(c[:, 0], c[:, 1])
    thick = 2 * half_thick(pod, node_s[tris].mean(axis=1)) * rim_taper(u * 1000, pod.rim)
    return nodes, tris, thick


def solve_plane_stress(nodes, tris, thick, f, fixed, E=1e7, nu=0.25):
    """Linear CST plane stress. Returns per-triangle [sx, sy, txy] (Pa). Stress is independent of E."""
    x, y = nodes[tris, 0], nodes[tris, 1]
    b = np.stack([y[:, 1] - y[:, 2], y[:, 2] - y[:, 0], y[:, 0] - y[:, 1]], 1)
    c = np.stack([x[:, 2] - x[:, 1], x[:, 0] - x[:, 2], x[:, 1] - x[:, 0]], 1)
    area2 = (x * b).sum(1)
    B = np.zeros((len(tris), 3, 6))
    B[:, 0, 0::2], B[:, 1, 1::2], B[:, 2, 0::2], B[:, 2, 1::2] = b, c, c, b
    B /= area2[:, None, None]
    Dm = E / (1 - nu**2) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])
    Ke = np.einsum("eki,kl,elj->eij", B, Dm, B) * (thick * area2 / 2)[:, None, None]
    dofs = np.stack([2 * tris, 2 * tris + 1], -1).reshape(-1, 6)
    ndof = 2 * len(nodes)
    K = coo_matrix((Ke.ravel(), (np.repeat(dofs, 6, 1).ravel(), np.tile(dofs, 6).ravel())),
                   shape=(ndof, ndof)).tocsr()
    free = np.setdiff1d(np.arange(ndof), fixed)
    u = np.zeros(ndof)
    u[free] = spsolve(K[free][:, free], f[free])
    return np.einsum("kl,elj,ej->ek", Dm, B, u[dofs])


COARSE, FINE = (360, 8), (1440, 32)  # FEM mesh (n_theta, n_r): search vs reported numbers


@lru_cache(maxsize=None)
def impact_stress(pod, exclude=0.003, mesh=COARSE):
    """Peak principal tension (Pa per kg/m^3 per m/s^2) when the pod lands edge-on on a lobe tip.

    The ground holds the lowest outer nodes; the pod's own decelerating mass loads it.
    Elements within `exclude` of the contact are skipped: that zone crushes locally, it does not split.
    The COARSE mesh reads ~25% low but ranks designs the same as FINE (~5% below converged).
    ponytail: linear elastic 2D, edge-on landing only; flat and tilted landings need 3D FEM.
    """
    nodes, tris, thick = plane_mesh(pod, *mesh)
    x, y = nodes[tris, 0], nodes[tris, 1]
    w = thick * np.abs((x[:, 1] - x[:, 0]) * (y[:, 2] - y[:, 0]) - (x[:, 2] - x[:, 0]) * (y[:, 1] - y[:, 0])) / 2
    f = np.zeros(2 * len(nodes))
    np.add.at(f, 2 * tris + 1, -np.repeat(w / 3, 3).reshape(-1, 3))
    contact = np.argsort(nodes[:, 1])[:3]
    sig = solve_plane_stress(nodes, tris, thick, f, np.concatenate([2 * contact, 2 * contact + 1]))
    return _peak_tension(nodes, tris, sig, [contact[0]], exclude)


def squeeze_stress(pod, exclude=0.005, mesh=FINE):
    """Peak principal tension (Pa) per newton when the pod is squeezed edge-on between two flat
    boards, as in the crush test. Measured tensile strength / this = predicted crack load (N)."""
    nodes, tris, thick = plane_mesh(pod, *mesh)
    bot, top = board_nodes(nodes, top=False), board_nodes(nodes, top=True)
    f = np.zeros(2 * len(nodes))
    f[2 * top + 1] = -1 / len(top)
    sig = solve_plane_stress(nodes, tris, thick, f, np.concatenate([2 * bot, 2 * bot + 1, [2 * top[0]]]))
    return _peak_tension(nodes, tris, sig, [*bot, *top], exclude)


def board_nodes(nodes, top, tol=1e-5):
    """Nodes touching a flat board pressed on the bottom or top: every node within tol (m) of the extreme,
    so an odd-lobe pod is held at both of the tips that touch one board, not at one of them."""
    y = nodes[:, 1] * (1 if top else -1)
    return np.flatnonzero(y >= y.max() - tol)


def _peak_tension(nodes, tris, sig, contacts, exclude):
    """Largest principal tension outside `exclude` (m) of the contact nodes, which crush rather than split."""
    s1 = (sig[:, 0] + sig[:, 1]) / 2 + np.hypot((sig[:, 0] - sig[:, 1]) / 2, sig[:, 2])
    c = nodes[tris].mean(1)
    far = np.all([np.linalg.norm(c - nodes[k], axis=1) > exclude for k in contacts], axis=0)
    return s1[far].max()


# ---------- rolling on edge (rimless-wheel model) ----------

def roll_polygon(pts, k2, v0, cap):
    """Distance (m) a rigid body rolls over its convex outline `pts` (CCW, centre of mass at origin).

    Starts pivoting on pts[0] with centre-of-mass speed v0. Each new contact is a perfectly
    plastic impact (angular momentum about the new pivot conserved). k2 = I/m about the CM.
    ponytail: hard flat ground, no slip, no rolling resistance; sand would stop pods sooner.
    """
    A, P, B = pts, np.roll(pts, 1, 0), np.roll(pts, -1, 0)
    cross = lambda u, v: u[:, 0] * v[:, 1] - u[:, 1] * v[:, 0]
    rA2 = (A**2).sum(1)
    d_prev = np.abs(cross(P, A)) / np.linalg.norm(A - P, axis=1)  # CM height with edge P-A on the ground
    d_next = np.abs(cross(A, B)) / np.linalg.norm(B - A, axis=1)
    rise = np.sqrt(rA2) - d_prev  # climb needed to vault over pivot A
    ratio = np.maximum((k2 + (A * B).sum(1)) / (k2 + (B**2).sum(1)), 0)  # omega after / before impact at B
    mult = ratio**2 * (k2 + (B**2).sum(1)) / (k2 + rA2)  # KE after impact at B / KE just before
    gain = G * (d_prev - d_next)  # KE gained falling from edge P-A onto edge A-B (per unit mass)
    step = np.linalg.norm(B - A, axis=1)
    # Recurrence KE_{i+1} = mult_i * (KE_i + gain_i), solved in closed form per revolution:
    # with M_i = prod_{j<i} mult_j,  KE_i = M_i * (KE_0 + sum_{j<i} gain_j / M_j).
    M = np.concatenate([[1.0], np.cumprod(mult)[:-1]])
    KE = 0.5 * (k2 + rA2[0]) * v0**2 / rA2[0]
    dist = 0.0
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        acc = np.cumsum(gain / M)
        while True:
            ke = M * (KE + np.concatenate([[0.0], acc[:-1]]))
            stuck = np.flatnonzero(~(ke >= G * rise))  # nan (underflow) counts as stuck
            if stuck.size:
                return min(dist + step[: stuck[0]].sum(), cap)
            dist += step.sum()
            if dist >= cap:
                return cap
            KE = M[-1] * mult[-1] * (KE + acc[-1])


def roll_distance(pod, v0, cap, n_theta=1440):
    th = np.arange(n_theta) * 2 * np.pi / n_theta
    r = r_out(pod, th)
    pts = np.stack([r * np.cos(th), r * np.sin(th)], 1)
    hull = pts[ConvexHull(pts).vertices]
    hull = np.roll(hull, -np.argmax((hull**2).sum(1)), 0)  # start on a lobe tip
    _, m, inertia = mass_props(pod, 1.0)
    return roll_polygon(hull, inertia / m, v0, cap)


# ---------- other metrics ----------

def tip_barrier(pod):
    """Height (m) the centre of mass must rise to tip a flat-lying pod onto its edge (lowest path)."""
    V, _ = surface_mesh(pod)
    V = V[ConvexHull(V).vertices]
    al = np.radians(np.linspace(0, 90, 91))[:, None, None]
    ph = np.linspace(0, 2 * np.pi, 72, endpoint=False)[None, :, None]
    u = np.stack(np.broadcast_arrays(np.sin(al) * np.cos(ph), np.sin(al) * np.sin(ph), -np.cos(al)), -1)
    h = (u @ V.T).max(-1)  # CM height above the ground for each tilt and direction
    return (h.max(0) - h[0]).min()


def outline_radii(pod, n_theta=2880):
    """(smallest lobe-tip radius, smallest valley radius) of the outline, in mm."""
    th = np.arange(n_theta) * 2 * np.pi / n_theta
    dt = th[1]
    r = r_out(pod, th) * 1000
    r1 = (np.roll(r, -1) - np.roll(r, 1)) / (2 * dt)
    r2 = (np.roll(r, -1) - 2 * r + np.roll(r, 1)) / dt**2
    k = (r**2 + 2 * r1**2 - r * r2) / (r**2 + r1**2) ** 1.5
    return 1 / k.max(), (1 / -k.min() if k.min() < 0 else math.inf)


def cover_depth(pod, n_theta=360, n_s=41):
    """Deepest point (mm) a seed can sit below every surface: the Calligonum pocket."""
    th = np.arange(n_theta) * 2 * np.pi / n_theta
    s = np.linspace(0, 1, n_s)
    ri = pod.hole / 2000
    ro = r_out(pod, th)[:, None]
    r = ri + (ro - ri) * s
    h = half_thick(pod, s) * rim_taper((ro - r) * 1000, pod.rim)
    return np.minimum(np.minimum(h, r - ri), ro - r).max() * 1000


def evaluate(pod, cfg, full=True):
    """Objectives and constraint metrics. full=True: fine-mesh stress plus report-only extras (slow)."""
    mesh = FINE if full else COARSE
    vol, mass, _ = mass_props(pod, cfg.density * 1000)
    tip_r, valley_r = outline_radii(pod)
    th = np.arange(720) * 2 * np.pi / 720
    m = {
        "mass_g": mass * 1000,
        "cost_aed_material": mass * cfg.cost_per_kg,
        "roll_m": roll_distance(pod, cfg.v0, cfg.cap),
        "stress_rel": impact_stress(pod, mesh=mesh) / impact_stress(PLAIN, mesh=mesh),
        "cover_mm": cover_depth(pod),
        "wall_mm": (r_out(pod, th).min() * 1000 - pod.hole / 2) if pod.hole else math.inf,
        "max_thick_mm": pod.t_edge + 2 * pod.dome,
        "tip_r_mm": tip_r,
        "valley_r_mm": valley_r,
        "hole_area_mm2": math.pi * pod.hole**2 / 4,
    }
    if full:
        V, F = surface_mesh(pod)
        area = np.linalg.norm(np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]]), axis=1).sum() / 2
        m["tip_barrier_mm"] = tip_barrier(pod) * 1000
        m["sa_per_vol_1_per_mm"] = area / vol / 1000
    return m


def constraints(m, cfg):
    """<= 0 means satisfied."""
    return [cfg.cover_min - m["cover_mm"], cfg.wall_min - m["wall_mm"],
            cfg.tip_r_min - m["tip_r_mm"], cfg.valley_r_min - min(m["valley_r_mm"], 1e3)]


def scaled(pod, k):
    """The same pod k times bigger in every direction (all mm settings; lobe count and profile unchanged)."""
    return replace(pod, D=pod.D * k, hole=pod.hole * k, t_edge=pod.t_edge * k, dome=pod.dome * k, a=pod.a * k,
                   rim=pod.rim * k)


def to_pod(x):
    return Pod(D=x[0], hole=x[1], t_edge=x[2], dome=x[3], n=int(round(x[4])), a=x[5], p=x[6])


PLAIN = Pod(D=30, hole=10, t_edge=10, dome=0, n=0, a=0, p=1)  # stress reference: plain 30/10 x 10 mm ring
DISC = Pod(D=30, hole=0, t_edge=10, dome=0, n=0, a=0, p=1)  # flat 30 x 10 mm disc (crush-test sample)


def pick_spread(F, k):
    """k Pareto points: the best all-rounder first, then each next one farthest from those chosen."""
    Z = (F - F.min(0)) / np.maximum(np.ptp(F, 0), 1e-12)
    chosen = [int(np.argmin(Z.sum(1)))]
    while len(chosen) < min(k, len(F)):
        d = np.min(np.linalg.norm(Z[:, None] - Z[chosen][None], axis=2), axis=1)
        chosen.append(int(np.argmax(d)))
    return chosen


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--density", type=float, default=1.2, help="dry pod density, g/cm^3 (PLACEHOLDER: measure yours)")
    ap.add_argument("--cost-per-kg", type=float, default=3.0, help="mix material cost, AED/kg (PLACEHOLDER: use quotes)")
    ap.add_argument("--v0", type=float, default=1.0, help="rolling speed left after landing, m/s (PLACEHOLDER)")
    ap.add_argument("--cap", type=float, default=2.0, help="roll distance reported as 'rolls away', m")
    ap.add_argument("--cover-min", type=float, default=4.0, help="min Calligonum pocket depth, mm")
    ap.add_argument("--wall-min", type=float, default=4.0, help="min ring wall (hole to crimp valley), mm")
    ap.add_argument("--tip-r-min", type=float, default=1.0, help="min lobe tip radius (anti-chipping), mm")
    ap.add_argument("--valley-r-min", type=float, default=0.5, help="min valley radius (press tooling), mm")
    ap.add_argument("--hole-min", type=float, default=BOUNDS["hole"][0], help="min hole diameter, mm")
    ap.add_argument("--pop", type=int, default=80)
    ap.add_argument("--gens", type=int, default=60)
    ap.add_argument("--picks", type=int, default=5)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", default="geometry/out")
    cfg = ap.parse_args(argv)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import ElementwiseProblem
    from pymoo.optimize import minimize

    out = Path(cfg.out)
    out.mkdir(parents=True, exist_ok=True)
    lo = np.array([v[0] for v in BOUNDS.values()], float)
    hi = np.array([v[1] for v in BOUNDS.values()], float)
    lo[1] = cfg.hole_min
    hi[4] += 0.49  # so rounding reaches the top lobe count

    class PodProblem(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=7, n_obj=3, n_ieq_constr=4, xl=lo, xu=hi)

        def _evaluate(self, x, res, *args, **kwargs):
            m = evaluate(to_pod(x), cfg, full=False)
            res["F"] = [m["mass_g"], m["roll_m"], m["stress_rel"]]
            res["G"] = constraints(m, cfg)

    res = minimize(PodProblem(), NSGA2(pop_size=cfg.pop), ("n_gen", cfg.gens), seed=cfg.seed, verbose=False)
    if res.X is None:
        raise SystemExit("No design met every constraint. Loosen --cover-min / --wall-min or widen BOUNDS.")
    X, F = np.atleast_2d(res.X), np.atleast_2d(res.F)
    pods = [to_pod(x) for x in X]
    keep = np.unique([tuple(asdict(p).values()) for p in pods], axis=0, return_index=True)[1]
    pods, F = [pods[i] for i in sorted(keep)], F[sorted(keep)]
    metrics = [evaluate(p, cfg) for p in pods]
    F = np.array([[m["mass_g"], m["roll_m"], m["stress_rel"]] for m in metrics])  # fine-mesh numbers
    picks = pick_spread(F, cfg.picks)

    with open(out / "pareto.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["pick", *asdict(pods[0]), *metrics[0]])
        for i, (p, m) in enumerate(zip(pods, metrics)):
            tag = picks.index(i) + 1 if i in picks else ""
            w.writerow([tag, *asdict(p).values(), *(round(v, 4) for v in m.values())])

    for rank, i in enumerate(picks, 1):
        write_stl(out / f"pick_{rank}.stl", *surface_mesh(pods[i], n_theta=720, n_s=48))

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    for k, (j, label) in enumerate([(1, "roll distance on edge (m)"), (2, "impact stress vs plain ring")]):
        sc = ax[k].scatter(F[:, 0], F[:, j], c=F[:, 3 - j], cmap="viridis", s=18)
        ax[k].scatter(F[picks, 0], F[picks, j], facecolors="none", edgecolors="crimson", s=110, lw=1.5)
        for rank, i in enumerate(picks, 1):
            ax[k].annotate(str(rank), (F[i, 0], F[i, j]), xytext=(5, 5), textcoords="offset points", color="crimson")
        ax[k].set_xlabel("mass per pod (g)")
        ax[k].set_ylabel(label)
        fig.colorbar(sc, ax=ax[k], label="impact stress vs plain ring" if j == 1 else "roll distance (m)")
    fig.suptitle(f"TerraPod crimped ring: {len(F)} Pareto-optimal designs (picks circled)")
    fig.tight_layout()
    fig.savefig(out / "pareto.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(2, len(picks), figsize=(3 * len(picks), 5.5), squeeze=False)
    th = np.linspace(0, 2 * np.pi, 721)
    for k, i in enumerate(picks):
        p, ro, ri = pods[i], r_out(pods[i], th) * 1000, pods[i].hole / 2
        ax[0, k].fill(ro * np.cos(th), ro * np.sin(th), color="#c9a77c")
        ax[0, k].fill(ri * np.cos(th), ri * np.sin(th), color="w")
        ax[0, k].set_title(f"pick {k + 1}: {p.n} lobes, {metrics[i]['mass_g']:.1f} g", fontsize=9)
        s = np.linspace(0, 1, 50)
        r, h = ri + (p.D / 2 - ri) * s, half_thick(p, s) * 1000
        for sign in (1, -1):
            ax[1, k].fill_between(sign * r, h, -h, color="#c9a77c")
        ax[1, k].set_title("cross-section through a lobe (mm)", fontsize=8)
        for a_ in ax[:, k]:
            a_.set_aspect("equal")
            a_.set_xlim(-15, 15)
        ax[0, k].set_ylim(-15, 15)
        ax[1, k].set_ylim(-9, 9)
    fig.tight_layout()
    fig.savefig(out / "picks.png", dpi=130)
    plt.close(fig)

    base = {"flat disc 30x10 (no hole)": DISC, "plain ring 30/10x10": PLAIN}
    cols = ["mass_g", "cost_aed_material", "roll_m", "stress_rel", "cover_mm", "max_thick_mm",
            "tip_barrier_mm", "sa_per_vol_1_per_mm"]
    lines = [
        "# TerraPod geometry search: results", "",
        f"NSGA-II, population {cfg.pop}, {cfg.gens} generations, seed {cfg.seed}. "
        f"{len(F)} Pareto-optimal designs; {len(picks)} picked for printing (`pick_N.stl`).", "",
        "**Assumptions to replace with measurements:** "
        f"density {cfg.density} g/cm³, material cost AED {cfg.cost_per_kg}/kg, "
        f"rolling speed after landing {cfg.v0} m/s. Constraints: Calligonum pocket ≥ {cfg.cover_min} mm, "
        f"wall ≥ {cfg.wall_min} mm, lobe tip radius ≥ {cfg.tip_r_min} mm, valley radius ≥ {cfg.valley_r_min} mm, "
        f"hole ≥ {cfg.hole_min} mm.", "",
        f"`roll_m` = {cfg.cap} means it does not stop by itself (the model has no sand friction). "
        "`stress_rel` < 1 means less peak tension than a plain 30/10 x 10 mm ring landing on its edge "
        "(fine-mesh FEM). A solid disc has no comparable value: its peak sits in the crushed contact zone.", "",
        "| design | " + " | ".join(asdict(DISC)) + " | " + " | ".join(cols) + " |",
        "|---" * (1 + len(asdict(DISC)) + len(cols)) + "|",
    ]
    for rank, i in enumerate(picks, 1):
        p, m = pods[i], metrics[i]
        lines.append(f"| pick {rank} | " + " | ".join(f"{v:.2f}" if isinstance(v, float) else str(v)
                                                       for v in asdict(p).values())
                     + " | " + " | ".join(f"{m[c]:.3f}" for c in cols) + " |")
    for name, p in base.items():
        m = evaluate(p, cfg)
        if p.hole == 0:
            m["stress_rel"] = math.nan
        lines.append(f"| {name} | " + " | ".join(str(v) for v in asdict(p).values())
                     + " | " + " | ".join(f"{m[c]:.3f}" for c in cols) + " |")
    (out / "summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return pods, F, picks


if __name__ == "__main__":
    main()
