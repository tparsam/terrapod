# Up-and-down rim waves: 3D landing test

200 identical random landings per design: random orientation, sideways 0.5 to 2 m/s, downward 0.5 to 2 m/s, spin 0 to 30 rad/s, starting 1 mm above hard flat ground (friction 0.6). MuJoCo 3.2.7, rigid pod, density 1.2 g/cm³. Ranks shapes only: sand stops every pod sooner.

`beats_pick1_pct`: share of the same landings where this design travelled less than pick 1. `face_gap_mm`: gap between a flat face and the ground at the rim when the pod lies on its wave crests (seeds on that face lose soil contact).

`ends_on_edge`: share of landings where the pod came to rest standing on its edge (no seeded face on the ground).

| design | median (cm) | 90th pct (cm) | mean (cm) | ends flat | ends on edge | beats pick 1 | mass (g) | face gap (mm) |
|---|---|---|---|---|---|---|---|---|
| pick 1 (4 lobes), no waves | 14.2 | 37.0 | 16.8 | 75% | 25% | 0% | 3.38 | 0.0 |
| pick 1 + 4 waves x 1.5 mm | 18.2 | 42.2 | 20.4 | 76% | 24% | 23% | 3.38 | 3.0 |
| pick 1 + 8 waves x 0.75 mm | 15.6 | 36.4 | 17.4 | 76% | 24% | 41% | 3.38 | 1.5 |
| pick 1 + 8 waves x 1.5 mm | 14.3 | 37.9 | 18.4 | 75% | 25% | 35% | 3.38 | 3.0 |
| pick 1 + 12 waves x 1.0 mm | 15.6 | 37.3 | 18.0 | 67% | 33% | 34% | 3.38 | 2.0 |
| smooth ring, no waves | 105.0 | 340.5 | 133.9 | 33% | 0% | 20% | 4.42 | 0.0 |
| smooth ring + 8 waves x 1.5 mm (pie crust) | 31.6 | 245.6 | 88.5 | 56% | 0% | 20% | 4.42 | 3.0 |
| 16 in-plane teeth x 1.5 mm | 27.0 | 92.3 | 38.2 | 62% | 8% | 20% | 3.88 | 0.0 |
| pick 1, rounded rim 2.5 mm | 12.5 | 32.9 | 15.4 | 100% | 0% | 55% | 3.16 | 0.0 |
| pick 1, rounded rim 2.5 mm + 8 waves x 0.75 mm | 13.7 | 33.8 | 16.2 | 100% | 0% | 48% | 3.16 | 1.5 |

Moulds written for the best wavy variant (pick 1 + 8 waves x 1.5 mm): `pick_1_waves_8x1.5mm_top_mould_half.stl` and `pick_1_waves_8x1.5mm_bottom_mould_half.stl` (print one of each; the bottom half flips onto the top). Pod: `pick_1_waves_8x1.5mm.stl`.
