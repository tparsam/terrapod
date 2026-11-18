# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib", "pymoo>=0.6"]
# ///
"""Two-part press moulds for the picked pods, the smooth-ring control and a crush-test disc.

Each pod is symmetric top to bottom, so both halves are the SAME part: print it twice, flip one
over (turn it 180 degrees about the axis through its peg-to-socket edge) and the pegs meet the sockets.

Run after pod_ga.py:  uv run geometry/moulds.py
"""
import csv
import dataclasses
import sys
from pathlib import Path

import numpy as np

import pod_ga as pg

PEG_R, PEG_H = 2.0, 3.0          # mm
SOCKET_R, SOCKET_D = 2.3, 3.5    # mm: 0.3 mm clearance, 0.5 mm deeper than the peg


def mould_half(pod, step=0.15, margin=8.0, base=3.0, pegs=True, wave=(0, 0.0), side=1):
    """Heightfield block (mm) with half the pod as a cavity in its top face.

    wave = (m, b) adds up-and-down rim waves (pod_ga.wave_lift). The halves then differ:
    side=1 is the top half, side=-1 the bottom half (mirrored, because it is flipped onto the top).
    A rounded outer rim (pod.rim) is moulded in too.
    Returns vertices (m), faces, (width, height) in m. ponytail: cavity walls are sampled on a
    `step` grid, so they are stair-stepped at that size; 0.15 mm is below an FDM nozzle's width.
    """
    width = pod.D + 2 * margin
    N = int(round(width / step)) + 1
    x = np.linspace(-width / 2, width / 2, N)
    X, Y = np.meshgrid(x, x)  # row i = y, column j = x
    r, th = np.hypot(X, Y), np.arctan2(Y, side * X)
    ri, ro = pod.hole / 2, pg.r_out(pod, th) * 1000
    inside = (r >= ri) & (r <= ro)
    s = np.clip((r - ri) / np.maximum(ro - ri, 1e-9), 0, 1)
    lift = pg.wave_lift(th, s, *wave) * 1000
    taper = pg.rim_taper(ro - r, pod.rim)  # ro, r in mm here
    depth = np.where(inside, pg.half_thick(pod, s) * 1000 * taper + side * lift, 0.0)
    height = base + depth.max()
    Z = height - depth
    if pegs:
        c = width / 2 - 4
        for sx, sy, dz, rad in [(1, 1, PEG_H, PEG_R), (-1, -1, PEG_H, PEG_R),
                                (-1, 1, -SOCKET_D, SOCKET_R), (1, -1, -SOCKET_D, SOCKET_R)]:
            Z = np.where(np.hypot(X - sx * c, Y - sy * c) <= rad, height + dz, Z)

    top = np.stack([X, Y, Z], -1).reshape(-1, 3)
    idx = np.arange(N * N).reshape(N, N)
    a, b, c_, d = idx[:-1, :-1], idx[:-1, 1:], idx[1:, 1:], idx[1:, :-1]
    F_top = np.concatenate([np.stack([a, b, c_], -1).reshape(-1, 3), np.stack([a, c_, d], -1).reshape(-1, 3)])
    ring = np.concatenate([idx[0, :-1], idx[:-1, -1], idx[-1, :0:-1], idx[:0:-1, 0]])  # CCW seen from above
    nb = len(ring)
    bottom = top[ring] * [1, 1, 0]
    centre = len(top) + nb
    V = np.vstack([top, bottom, [[0.0, 0.0, 0.0]]])
    p, q = np.arange(nb), (np.arange(nb) + 1) % nb
    bp, bq, tp, tq = len(top) + p, len(top) + q, ring[p], ring[q]
    F_side = np.concatenate([np.stack([bp, bq, tq], 1), np.stack([bp, tq, tp], 1)])
    F_bot = np.stack([np.full(nb, centre), bq, bp], 1)
    F = np.concatenate([F_top, F_side, F_bot])
    return V / 1000, F, (width / 1000, height / 1000)


def load_pods(out):
    """The test set: every pick from pareto.csv, a smooth-ring control (pick 1 without crimps), a crush disc."""
    rows = sorted((r for r in csv.DictReader(open(out / "pareto.csv")) if r["pick"]), key=lambda r: int(r["pick"]))
    pods = {f"pick_{r['pick']}": pg.Pod(float(r["D"]), float(r["hole"]), float(r["t_edge"]), float(r["dome"]),
                                       int(r["n"]), float(r["a"]), float(r["p"])) for r in rows}
    p1 = pods["pick_1"]
    pods["control_smooth_ring"] = pg.Pod(p1.D, p1.hole, p1.t_edge, p1.dome, 0, 0, 1)
    pods["crush_test_disc"] = pg.Pod(D=30, hole=0, t_edge=10, dome=0, n=0, a=0, p=1)
    pods["pick_1_rounded_rim"] = dataclasses.replace(p1, rim=2.5)  # stops resting on edge (waves3d.py)
    return pods


def main(argv=None):
    out = Path(argv[0] if argv else "geometry/out")
    pods = load_pods(out)
    mdir = out / "moulds"
    mdir.mkdir(parents=True, exist_ok=True)
    lines = ["# Press moulds", "",
             "Print each file **twice** (both halves are the same part). Pod volume is what you divide "
             "a dried pod's mass by to get `--density`.", "",
             "| mould | pod settings (D / hole / t_edge / dome / n / a / p) | pod volume (cm³) | block (mm) |",
             "|---|---|---|---|"]
    for name, pod in pods.items():
        V, F, (side, height) = mould_half(pod)
        pg.write_stl(mdir / f"{name}_mould_half.stl", V, F)
        vol = pg.mass_props(pod, 1000)[0] * 1e6
        settings = " / ".join(f"{v:g}" if isinstance(v, int) else f"{v:.2f}" for v in vars(pod).values())
        lines.append(f"| `{name}_mould_half.stl` | {settings} | {vol:.3f} | "
                     f"{side * 1000:.0f} x {side * 1000:.0f} x {height * 1000:.1f} (+{PEG_H:g} pegs) |")
    (mdir / "moulds.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1:])
