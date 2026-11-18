# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "scipy", "matplotlib", "pymoo>=0.6"]
# ///
"""Turn the bench-test datasheet into deck numbers and check them against the model.

Run:  uv run geometry/analyse_tests.py geometry/test_data.csv
Fill the CSV following geometry/TEST_PROTOCOL.md (one row per pod per test).
"""
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

import moulds
import pod_ga as pg

IMPACT_SPEED = 16.0  # m/s at the ground after a 15 m fall with drag (research.md section 8)

COLUMNS = ["design", "pod_id", "test", "surface", "mass_dry_g", "diameter_mm", "thickness_mm",
           "peak_kg", "result", "embed_mm", "roll_cm", "mass_after_g", "soften_min", "dry_hours", "notes"]


def drop_estimate(pod, tensile_kpa, density):
    """(hardest edge-on stop the pod survives in g, ground give needed at IMPACT_SPEED in mm).

    Edge-on landing: peak tension = density x deceleration x impact_stress(pod). Loose desert sand
    gives roughly 10 to 30 mm; gravel or crusted ground a few mm. ponytail: assumes constant deceleration.
    """
    a = tensile_kpa * 1000 / (density * 1000 * pg.impact_stress(pod, mesh=pg.FINE))
    return a / pg.G, IMPACT_SPEED**2 / (2 * a) * 1000


def _num(row, key):
    v = (row.get(key) or "").strip()
    return float(v) if v else None


def analyse(path, pods):
    """Per-design summary: density, crush strength/load, drop survival, roll, tumble loss, softening."""
    rows = list(csv.DictReader(open(path, newline="")))
    unknown = {r["design"] for r in rows} - set(pods)
    if unknown:
        raise SystemExit(f"Unknown design name(s) in {path}: {sorted(unknown)}. Use: {sorted(pods)}")
    acc = defaultdict(lambda: defaultdict(list))
    for r in rows:
        pod, a = pods[r["design"]], acc[r["design"]]
        mass, diam, thick, kg = (_num(r, k) for k in ("mass_dry_g", "diameter_mm", "thickness_mm", "peak_kg"))
        if mass and diam:  # shrinkage-corrected volume: model volume scaled by measured/nominal diameter cubed
            a["density_g_cm3"].append(mass / (pg.mass_props(pod, 1000)[0] * 1e6 * (diam / pod.D) ** 3))
        test = r["test"].strip().lower()
        if test == "crush" and kg:
            a["crush_load_n"].append(kg * pg.G)
            if pod.hole == 0 and pod.a == 0 and diam and thick:  # Brazilian test: 2P / (pi D t)
                a["tensile_kpa"].append(2 * kg * pg.G / (math.pi * diam * thick * 1e-6) / 1000)
        elif test == "drop":
            surface = r["surface"].strip().lower()
            a[f"drop_{surface}_survival_pct"].append(100.0 * (r["result"].strip().lower() == "intact"))
            if _num(r, "embed_mm") is not None:  # how deep the pod sank: buried seed beats surface seed
                a[f"drop_{surface}_embed_mm"].append(_num(r, "embed_mm"))
        elif test == "roll" and _num(r, "roll_cm") is not None:
            a["roll_cm"].append(_num(r, "roll_cm"))
        elif test == "tumble" and mass and _num(r, "mass_after_g") is not None:
            a["tumble_loss_pct"].append(100 * (mass - _num(r, "mass_after_g")) / mass)
        elif test == "drying" and _num(r, "dry_hours") is not None:
            a["dry_hours"].append(_num(r, "dry_hours"))
        elif test == "fan":
            a["fan_stayed_pct"].append(100.0 * (r["result"].strip().lower() == "stayed"))
        elif test == "soak" and _num(r, "soften_min") is not None:
            a["soften_min"].append(_num(r, "soften_min"))
    return {d: {k: float(np.mean(v)) for k, v in a.items()} | {"n_rows": sum(len(v) for v in a.values())}
            for d, a in acc.items()}


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    data = Path(argv[0] if argv else "geometry/test_data.csv")
    out = Path(argv[1] if len(argv) > 1 else "geometry/out")
    pods = moulds.load_pods(out)
    res = analyse(data, pods)
    keys = sorted({k for v in res.values() for k in v if k != "n_rows"})
    lines = [f"# Bench test results ({data.name})", "", "| design | " + " | ".join(keys) + " |",
             "|---" * (len(keys) + 1) + "|"]
    for d, v in res.items():
        lines.append(f"| {d} | " + " | ".join(f"{v[k]:.2f}" if k in v else "" for k in keys) + " |")

    tensile = res.get("crush_test_disc", {}).get("tensile_kpa")
    if tensile:
        dens_all = [v["density_g_cm3"] for v in res.values() if "density_g_cm3" in v]
        lines += ["", f"## Crack load and drop estimate (mix tensile strength {tensile:.1f} kPa)", "",
                  "Crack load: squeezed edge-on between boards, as in the crush test. Drop estimate: the "
                  f"hardest edge-on stop the pod survives, and the ground give it needs at {IMPACT_SPEED:g} m/s "
                  "(loose desert sand gives roughly 10 to 30 mm, gravel or crusted ground a few mm).", "",
                  "| design | predicted crack (kg) | measured crack (kg) | survives up to (g) | needs ground give (mm) |",
                  "|---|---|---|---|---|"]
        for d, pod in pods.items():
            if pod.hole == 0:
                continue
            pred = tensile * 1000 / pg.squeeze_stress(pod) / pg.G
            meas = res.get(d, {}).get("crush_load_n")
            rho = res.get(d, {}).get("density_g_cm3") or (np.mean(dens_all) if dens_all else None)
            g_max, stop = drop_estimate(pod, tensile, rho) if rho else (math.nan, math.nan)
            lines.append(f"| {d} | {pred:.2f} | {f'{meas / pg.G:.2f}' if meas else ''} | {g_max:.0f} | {stop:.1f} |")

    rolled = [d for d in res if "roll_cm" in res[d] and pods[d].hole]
    if len(rolled) >= 3:
        model = [pg.roll_distance(pods[d], 1.0, 2.0) for d in rolled]
        rho = spearmanr(model, [res[d]["roll_cm"] for d in rolled]).statistic
        lines += ["", f"## Roll ranking: model vs ramp test", "",
                  f"Spearman rank agreement {rho:+.2f} over {len(rolled)} designs "
                  "(+1 = same order as the model, 0 = unrelated, -1 = reversed)."]

    dens = [v["density_g_cm3"] for v in res.values() if "density_g_cm3" in v]
    if dens:
        lines += ["", "## Re-run the search with your density", "",
                  f"`uv run geometry/pod_ga.py --density {np.mean(dens):.2f} --cost-per-kg <AED/kg from quotes>`"]
    (out / "test_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return res


if __name__ == "__main__":
    main()
