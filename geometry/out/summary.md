# TerraPod geometry search: results

NSGA-II, population 80, 60 generations, seed 1. 80 Pareto-optimal designs; 5 picked for printing (`pick_N.stl`).

**Assumptions to replace with measurements:** density 1.2 g/cm³, material cost AED 3.0/kg, rolling speed after landing 1.0 m/s. Constraints: Calligonum pocket ≥ 4.0 mm, wall ≥ 4.0 mm, lobe tip radius ≥ 1.0 mm, valley radius ≥ 0.5 mm, hole ≥ 6.0 mm.

`roll_m` = 2.0 means it does not stop by itself (the model has no sand friction). `stress_rel` < 1 means less peak tension than a plain 30/10 x 10 mm ring landing on its edge (fine-mesh FEM). A solid disc has no comparable value: its peak sits in the crushed contact zone.

| design | D | hole | t_edge | dome | n | a | p | mass_g | cost_aed_material | roll_m | stress_rel | cover_mm | max_thick_mm | tip_barrier_mm | sa_per_vol_1_per_mm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pick 1 | 25.02 | 6.00 | 7.69 | 0.20 | 4 | 2.98 | 0.96 | 3.386 | 0.010 | 0.108 | 0.491 | 4.043 | 8.086 | 6.853 | 0.505 |
| pick 2 | 25.07 | 7.44 | 4.03 | 2.02 | 3 | 2.98 | 0.81 | 2.652 | 0.008 | 0.497 | 0.679 | 4.036 | 8.072 | 5.755 | 0.530 |
| pick 3 | 25.01 | 8.93 | 4.05 | 2.00 | 5 | 2.98 | 0.87 | 2.506 | 0.008 | 0.089 | 0.888 | 4.018 | 8.061 | 6.809 | 0.574 |
| pick 4 | 25.00 | 6.00 | 10.85 | 0.00 | 3 | 2.99 | 0.83 | 4.533 | 0.014 | 0.401 | 0.463 | 4.751 | 10.848 | 5.552 | 0.443 |
| pick 5 | 25.00 | 6.01 | 10.83 | 2.15 | 5 | 3.00 | 0.87 | 5.696 | 0.017 | 0.088 | 0.573 | 4.748 | 15.132 | 4.376 | 0.391 |
| flat disc 30x10 (no hole) | 30 | 0 | 10 | 0 | 0 | 0 | 1 | 8.482 | 0.025 | 2.000 | nan | 5.000 | 10.000 | 10.810 | 0.333 |
| plain ring 30/10x10 | 30 | 10 | 10 | 0 | 0 | 0 | 1 | 7.540 | 0.023 | 2.000 | 1.000 | 5.000 | 10.000 | 10.810 | 0.400 |
