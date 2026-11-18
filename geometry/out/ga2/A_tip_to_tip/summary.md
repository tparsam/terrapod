# GA v2, scenario A_tip_to_tip

NSGA-II, population 60, 40 generations, 60 search landings per design. Picks and the current lead re-scored on 200 landings (the waves3d.py set) with the fine-mesh FEM.

58 designs on the trade-off front.

Rules: Calligonum pocket >= 4.0 mm, wall >= 4.0 mm, lobe tip radius >= 1.0 mm, valley radius >= 0.5 mm, rests on edge <= 5.0% of landings, hole narrower than the ring's thickness and wall (no hooking). Density 1.2 g/cm³ (placeholder).

| design | meets rules | D | hole | t_edge | dome | n | a | p | rim | mass_g | travel_median_cm | travel_p90_cm | on_edge_pct | stress_rel | cover_mm | narrowest_width_mm | max_thick_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **current lead** | yes | 25.02 | 6 | 7.69 | 0.20 | 4 | 2.98 | 0.96 | 2.50 | 3.17 | 12.62 | 31.61 | 0.50 | 0.48 | 4.04 | 20.38 | 8.09 |
| pick 1 | yes | 25.52 | 6.00 | 8.08 | 0.03 | 4 | 2.96 | 0.98 | 3.08 | 3.37 | 12.81 | 30.28 | 2.50 | 0.47 | 4.07 | 20.88 | 8.14 |
| pick 2 | yes | 29.35 | 6.11 | 7.80 | 0.17 | 4 | 2.95 | 1.01 | 3.42 | 4.67 | 13.33 | 31.07 | 0.50 | 0.53 | 4.07 | 24.42 | 8.15 |
| pick 3 | yes | 26.17 | 6.07 | 8.37 | 0.00 | 3 | 2.96 | 0.94 | 3.21 | 3.66 | 18.19 | 40.12 | 0.50 | 0.46 | 4.19 | 23.27 | 8.38 |
| pick 4 | yes | 26.13 | 6.68 | 7.81 | 0.13 | 6 | 2.99 | 1.09 | 3.04 | 3.48 | 12.96 | 34.81 | 0.50 | 0.60 | 4.03 | 23.46 | 8.07 |

Files: `pick_N.stl` (pod), `pick_N_mould_half.stl` (press mould, print twice), `pareto.csv`, `pareto.png`.
