# /// script
# requires-python = ">=3.10,<3.12"
# dependencies = ["numpy", "scipy", "matplotlib", "pymoo>=0.6", "mujoco<3.3"]
# ///
"""Mix-wise designs: Mix A and Mix B picks from ga2.py, plus each Mix B ring turned into a lobed disc
(same outline, no hole), all scored on the same 200 landings and the same squeeze test.

Also writes the print-ready moulds of the final designs (out/print/): each pod scaled up so that it is
still >= --dried-min mm tip to tip after drying, then enlarged by the drying shrinkage.

Run after ga2.py has written geometry/out/ga2_mixA and ga2_mixB:
    uv run --python 3.11 geometry/mix_compare.py [--shrink 0.05] [--dried-min 26]
"""
import argparse
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


def print_scale(pod, dried_min, shrink):
    """(dried pod, mould pod): the dried pod is >= dried_min mm tip to tip; the mould is shrink bigger."""
    dried = pg.scaled(pod, max(1.0, dried_min / pod.D))
    return dried, pg.scaled(dried, 1 / (1 - shrink))


def write_print_set(finals, dried_min, shrink):
    out = OUT / "print"
    out.mkdir(exist_ok=True)
    lines = ["# Print-ready moulds (final designs)", "",
             f"Each pod is scaled so it is still at least **{dried_min:g} mm tip to tip after drying** (the rule is "
             f"2.5 to 3 cm; the margin covers press and drying scatter), then the mould is enlarged by an assumed "
             f"**{shrink:.0%} linear drying shrinkage** (PLACEHOLDER). Press one test pod, measure its dried "
             "diameter, and re-run with the real value: `--shrink <1 - dried/mould>`. Print each mould **twice**.", "",
             "| mould | design | mould pod: D / hole / thick (mm) | dried pod: D / narrowest / hole / thick (mm) "
             "| dried mass (g, 1.2 g/cm³) |", "|---|---|---|---|---|"]
    for name, pod in finals.items():
        dried, mould = print_scale(pod, dried_min, shrink)
        f = f"{name}_mould_half.stl"
        pg.write_stl(out / f, *moulds.mould_half(mould)[:2])
        mass = pg.mass_props(dried, 1200)[1] * 1000
        lines.append(f"| `{f}` | {name.replace('_', ' ')} | {mould.D:.1f} / {mould.hole:.1f} / "
                     f"{mould.t_edge + 2 * mould.dome:.1f} | {dried.D:.1f} / {ga2.narrowest_width_mm(dried):.1f} / "
                     f"{dried.hole:.1f} / {dried.t_edge + 2 * dried.dome:.1f} | {mass:.2f} |")
    (out / "print.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--shrink", type=float, default=0.05, help="linear drying shrinkage (PLACEHOLDER: measure)")
    ap.add_argument("--dried-min", type=float, default=26.0, help="min dried tip-to-tip diameter, mm")
    cfg = ap.parse_args(argv)
    global SQ_LEAD
    SQ_LEAD = pg.squeeze_stress(ga2.LEAD)
    landings = w3.random_landings(200, seed=7)
    designs = {"current lead": ga2.LEAD, "old backup (5 lobes)": pick1(OUT / "ga2" / "B_narrowest_25mm")}
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
    write_print_set({k.replace(", ", "_").replace(" ", "_"): designs[k] for k in
                     ("Mix A, A_tip_to_tip", "Mix B disc, A_tip_to_tip", "Mix A, B_narrowest_25mm",
                      "Mix B disc, B_narrowest_25mm")}, cfg.dried_min, cfg.shrink)


if __name__ == "__main__":
    sys.exit(main())
