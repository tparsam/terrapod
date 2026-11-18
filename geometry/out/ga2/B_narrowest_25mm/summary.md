# GA v2, scenario B_narrowest_25mm

NSGA-II, population 60, 40 generations, 60 search landings per design. Picks and the current lead re-scored on 200 landings (the waves3d.py set) with the fine-mesh FEM.

59 designs on the trade-off front.

Rules: Calligonum pocket >= 4.0 mm, wall >= 4.0 mm, lobe tip radius >= 1.0 mm, valley radius >= 0.5 mm, rests on edge <= 5.0% of landings, hole narrower than the ring's thickness and wall (no hooking), narrowest width >= 25 mm. Density 1.2 g/cm³ (placeholder).

| design | meets rules | D | hole | t_edge | dome | n | a | p | rim | mass_g | travel_median_cm | travel_p90_cm | on_edge_pct | stress_rel | cover_mm | narrowest_width_mm | max_thick_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **current lead** | **no** | 25.02 | 6 | 7.69 | 0.20 | 4 | 2.98 | 0.96 | 2.50 | 3.17 | 12.62 | 31.61 | 0.50 | 0.48 | 4.04 | 20.38 | 8.09 |
| pick 1 | yes | 27.59 | 6.06 | 7.89 | 0.08 | 5 | 2.99 | 0.92 | 3.50 | 3.95 | 12.07 | 35.40 | 1.50 | 0.53 | 4.03 | 25.65 | 8.06 |
| pick 2 | yes | 25.64 | 6.49 | 7.91 | 0.05 | 9 | 2.97 | 1.24 | 3.35 | 3.37 | 15.11 | 42.76 | 1.00 | 0.66 | 4.01 | 25.01 | 8.02 |
| pick 3 | yes | 26.05 | 6.07 | 7.92 | 0.05 | 7 | 2.99 | 1.15 | 3.41 | 3.50 | 13.98 | 40.23 | 3.50 | 0.58 | 4.01 | 25.03 | 8.02 |
| pick 4 | yes | 29.21 | 6.08 | 8.28 | 0.01 | 6 | 3.00 | 1.04 | 3.44 | 4.76 | 12.23 | 37.14 | 2.00 | 0.58 | 4.15 | 26.24 | 8.29 |

Files: `pick_N.stl` (pod), `pick_N_mould_half.stl` (press mould, print twice), `pareto.csv`, `pareto.png`.
