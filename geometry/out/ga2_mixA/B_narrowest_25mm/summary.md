# GA v2, scenario B_narrowest_25mm

NSGA-II, population 60, 40 generations, 60 search landings per design. Picks and the current lead re-scored on 200 landings (the waves3d.py set) with the fine-mesh FEM.

53 designs on the trade-off front.

Rules: Calligonum pocket >= 3.0 mm, wall >= 4.0 mm, lobe tip radius >= 1.0 mm, valley radius >= 0.5 mm, rests on edge <= 5.0% of landings, hole narrower than the ring's thickness and wall (no hooking), narrowest width >= 25 mm. Density 1.2 g/cm³ (placeholder).

| design | meets rules | D | hole | t_edge | dome | n | a | p | rim | mass_g | travel_median_cm | travel_p90_cm | on_edge_pct | stress_rel | cover_mm | narrowest_width_mm | max_thick_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **current lead** | **no** | 25.02 | 6 | 7.69 | 0.20 | 4 | 2.98 | 0.96 | 2.50 | 3.17 | 12.62 | 31.61 | 0.50 | 0.48 | 4.04 | 20.38 | 8.09 |
| pick 1 | yes | 27.59 | 6.00 | 6.09 | 0.00 | 5 | 2.99 | 0.94 | 3.42 | 3.02 | 11.33 | 28.54 | 0.50 | 0.53 | 3.05 | 25.66 | 6.10 |
| pick 2 | yes | 28.12 | 6.00 | 6.22 | 0.00 | 3 | 2.99 | 0.89 | 3.33 | 3.22 | 15.17 | 36.79 | 0.00 | 0.48 | 3.11 | 25.14 | 6.22 |
| pick 3 | yes | 29.86 | 6.01 | 6.26 | 0.00 | 4 | 2.99 | 1.35 | 3.46 | 3.89 | 11.35 | 26.77 | 0.50 | 0.53 | 3.13 | 25.44 | 6.26 |
| pick 4 | yes | 28.76 | 6.01 | 6.13 | 0.00 | 6 | 2.99 | 0.93 | 3.26 | 3.37 | 11.49 | 28.87 | 0.00 | 0.57 | 3.06 | 25.65 | 6.13 |

Files: `pick_N.stl` (pod), `pick_N_mould_half.stl` (press mould, print twice), `pareto.csv`, `pareto.png`.
