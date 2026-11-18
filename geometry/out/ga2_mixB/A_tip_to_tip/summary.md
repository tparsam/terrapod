# GA v2, scenario A_tip_to_tip

NSGA-II, population 60, 40 generations, 60 search landings per design. Picks and the current lead re-scored on 200 landings (the waves3d.py set) with the fine-mesh FEM.

54 designs on the trade-off front.

Rules: Calligonum pocket >= 4.5 mm, wall >= 4.0 mm, lobe tip radius >= 1.0 mm, valley radius >= 0.5 mm, rests on edge <= 5.0% of landings, hole narrower than the ring's thickness and wall (no hooking). Density 1.2 g/cm³ (placeholder).

| design | meets rules | D | hole | t_edge | dome | n | a | p | rim | mass_g | travel_median_cm | travel_p90_cm | on_edge_pct | stress_rel | cover_mm | narrowest_width_mm | max_thick_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **current lead** | **no** | 25.02 | 6 | 7.69 | 0.20 | 4 | 2.98 | 0.96 | 2.50 | 3.17 | 12.62 | 31.61 | 0.50 | 0.48 | 4.04 | 20.38 | 8.09 |
| pick 1 | yes | 25.04 | 6.00 | 9.00 | 0.01 | 4 | 3.00 | 0.92 | 3.48 | 3.48 | 12.91 | 31.60 | 0.50 | 0.46 | 4.51 | 20.29 | 9.02 |
| pick 2 | yes | 25.01 | 6.02 | 9.13 | 0.01 | 3 | 2.99 | 0.82 | 3.33 | 3.49 | 19.61 | 41.23 | 1.50 | 0.44 | 4.57 | 22.05 | 9.15 |
| pick 3 | yes | 25.57 | 6.00 | 10.00 | 0.04 | 4 | 3.00 | 1.14 | 3.34 | 4.22 | 14.62 | 39.81 | 1.00 | 0.47 | 4.89 | 21.21 | 10.08 |
| pick 4 | yes | 25.51 | 6.27 | 8.43 | 0.30 | 6 | 2.94 | 0.91 | 3.46 | 3.57 | 14.35 | 36.83 | 1.50 | 0.57 | 4.51 | 22.67 | 9.03 |

Files: `pick_N.stl` (pod), `pick_N_mould_half.stl` (press mould, print twice), `pareto.csv`, `pareto.png`.
