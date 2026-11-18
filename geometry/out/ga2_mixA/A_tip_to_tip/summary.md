# GA v2, scenario A_tip_to_tip

NSGA-II, population 60, 40 generations, 60 search landings per design. Picks and the current lead re-scored on 200 landings (the waves3d.py set) with the fine-mesh FEM.

19 designs on the trade-off front.

Rules: Calligonum pocket >= 3.0 mm, wall >= 4.0 mm, lobe tip radius >= 1.0 mm, valley radius >= 0.5 mm, rests on edge <= 5.0% of landings, hole narrower than the ring's thickness and wall (no hooking). Density 1.2 g/cm³ (placeholder).

| design | meets rules | D | hole | t_edge | dome | n | a | p | rim | mass_g | travel_median_cm | travel_p90_cm | on_edge_pct | stress_rel | cover_mm | narrowest_width_mm | max_thick_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **current lead** | yes | 25.02 | 6 | 7.69 | 0.20 | 4 | 2.98 | 0.96 | 2.50 | 3.17 | 12.62 | 31.61 | 0.50 | 0.48 | 4.04 | 20.38 | 8.09 |
| pick 1 | yes | 25.09 | 6.01 | 6.15 | 0.00 | 4 | 2.99 | 0.98 | 3.40 | 2.42 | 11.26 | 27.72 | 0.50 | 0.46 | 3.08 | 20.47 | 6.16 |
| pick 2 | yes | 25.07 | 6.02 | 6.15 | 0.01 | 3 | 2.99 | 0.91 | 3.26 | 2.40 | 14.46 | 32.30 | 0.50 | 0.44 | 3.09 | 22.15 | 6.18 |
| pick 3 | yes | 26.41 | 6.09 | 6.44 | 0.02 | 4 | 2.99 | 0.89 | 3.20 | 2.87 | 11.70 | 26.88 | 1.00 | 0.49 | 3.24 | 21.47 | 6.49 |
| pick 4 | yes | 25.00 | 6.03 | 6.15 | 0.01 | 6 | 3.00 | 0.91 | 3.19 | 2.39 | 11.18 | 31.42 | 0.50 | 0.54 | 3.09 | 22.20 | 6.18 |

Files: `pick_N.stl` (pod), `pick_N_mould_half.stl` (press mould, print twice), `pareto.csv`, `pareto.png`.
