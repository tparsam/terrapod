# /// script
# requires-python = ">=3.10,<3.12"
# dependencies = ["numpy", "scipy", "matplotlib", "pymoo>=0.6", "mujoco<3.3"]
# ///
"""Mix-wise designs: Mix A and Mix B picks from ga2.py, plus each Mix B ring turned into a lobed disc
(same outline, no hole), all scored on the same 200 landings and the same squeeze test.

Run after ga2.py has written geometry/out/ga2_mixA and ga2_mixB:
    uv run --python 3.11 geometry/mix_compare.py
"""
import csv
import sys
from argparse import Namespace
from dataclasses import replace
from pathlib import Path

import ga2
import moulds
import pod_ga as pg
import waves3d as w3

OUT = Path(__file__).parent / "out"
CFG = Namespace(density=1.2, cost_per_kg=3.0, v0=1.0, cap=2.0)


def pick1(folder):
    with open(folder / "pareto.csv") as fh:
        row = next(r for r in csv.DictReader(fh) if r["pick"] == "1")
    return pg.Pod(*(float(row[k]) for k in ("D", "hole", "t_edge", "dome")), int(row["n"]),
                  *(float(row[k]) for k in ("a", "p", "rim")))


def row(name, pod, landings):
    m = pg.evaluate(pod, CFG)
    med, p90, edge = ga2.landings_3d(pod, *landings, fast=False)
    # crack load relative to the current lead in the crush test (same mix strength): higher = stronger
    return {"design": name, "D": pod.D, "hole": pod.hole, "t_edge": pod.t_edge, "n": pod.n, "rim": pod.rim,
            "mass_g": m["mass_g"], "max_thick_mm": m["max_thick_mm"], "cover_mm": m["cover_mm"],
            "narrowest_mm": ga2.narrowest_width_mm(pod), "travel_median_cm": med, "travel_p90_cm": p90,
            "on_edge_pct": edge, "crush_load_vs_lead": SQ_LEAD / pg.squeeze_stress(pod)}


def main():
    global SQ_LEAD
    SQ_LEAD = pg.squeeze_stress(ga2.LEAD)
    landings = w3.random_landings(200, seed=7)
    designs = {"current lead": ga2.LEAD}
    for scen in ga2.SCENARIOS:
        designs[f"Mix A, {scen}"] = pick1(OUT / "ga2_mixA" / scen)
        ring = pick1(OUT / "ga2_mixB" / scen)
        designs[f"Mix B ring, {scen}"] = ring
        designs[f"Mix B disc, {scen}"] = disc = replace(ring, hole=0.0)
        pg.write_stl(OUT / "ga2_mixB" / scen / "disc_version.stl", *pg.surface_mesh(disc, n_theta=720, n_s=48))
        pg.write_stl(OUT / "ga2_mixB" / scen / "disc_version_mould_half.stl", *moulds.mould_half(disc)[:2])
    rows = [row(k, p, landings) for k, p in designs.items()]
    cols = list(rows[0])
    lines = ["# Mix-wise designs", "",
             "Same 200 landings (waves3d.py set), hard ground. `crush_load_vs_lead` = load to crack it in the "
             "edge-on squeeze test, relative to the current lead, same mix (higher = stronger). Density 1.2 g/cm³ "
             "(placeholder).", "",
             "| " + " | ".join(cols) + " |", "|---" * len(cols) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(v if isinstance(v, str) else f"{v:.2f}" for v in r.values()) + " |")
    (OUT / "mix_designs.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
