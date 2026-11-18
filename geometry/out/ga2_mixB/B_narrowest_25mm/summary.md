# GA v2, scenario B_narrowest_25mm

NSGA-II, population 60, 40 generations, 60 search landings per design. Picks and the current lead re-scored on 200 landings (the waves3d.py set) with the fine-mesh FEM.

60 designs on the trade-off front.

Rules: Calligonum pocket >= 4.5 mm, wall >= 4.0 mm, lobe tip radius >= 1.0 mm, valley radius >= 0.5 mm, rests on edge <= 5.0% of landings, hole narrower than the ring's thickness and wall (no hooking), narrowest width >= 25 mm. Density 1.2 g/cm³ (placeholder).

| design | meets rules | D | hole | t_edge | dome | n | a | p | rim | mass_g | travel_median_cm | travel_p90_cm | on_edge_pct | stress_rel | cover_mm | narrowest_width_mm | max_thick_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **current lead** | **no** | 25.02 | 6 | 7.69 | 0.20 | 4 | 2.98 | 0.96 | 2.50 | 3.17 | 12.62 | 31.61 | 0.50 | 0.48 | 4.04 | 20.38 | 8.09 |
| pick 1 | yes | 27.39 | 6.01 | 6.85 | 1.10 | 5 | 2.83 | 1.02 | 3.45 | 4.14 | 12.68 | 34.42 | 1.00 | 0.58 | 4.52 | 25.57 | 9.04 |
| pick 2 | yes | 27.71 | 6.01 | 8.32 | 0.69 | 3 | 2.94 | 1.40 | 3.36 | 4.84 | 17.41 | 37.90 | 0.50 | 0.51 | 4.85 | 25.04 | 9.69 |
| pick 3 | yes | 26.14 | 6.31 | 6.60 | 1.27 | 9 | 2.86 | 1.06 | 3.48 | 3.66 | 14.59 | 34.25 | 1.00 | 0.70 | 4.57 | 25.45 | 9.15 |
| pick 4 | yes | 27.89 | 6.01 | 8.69 | 1.09 | 6 | 2.83 | 1.01 | 3.45 | 5.28 | 15.20 | 41.55 | 1.50 | 0.60 | 5.44 | 25.02 | 10.87 |

Files: `pick_N.stl` (pod), `pick_N_mould_half.stl` (press mould, print twice), `pareto.csv`, `pareto.png`.
