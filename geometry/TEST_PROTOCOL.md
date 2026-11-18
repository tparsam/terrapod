# TerraPod bench tests: protocol

These tests check the shape model against reality and give you the numbers the deck needs:
dry density, drop survival, roll distance, handling loss, softening time and mix strength.
Plan on **2 to 3 days**, mostly waiting for pods to dry. The germination trays are separate (`research.md` §15).

**You need:**
- 3D printer (PLA or PETG)
- kitchen scale (0.01 g)
- bathroom scale
- calipers or a ruler
- a board for a ramp (40 cm)
- a lidded plastic tub (about 2 L)
- a phone with slow-motion video
- a sand tray (20 cm deep)
- safety glasses

## 1. Print the moulds

Files are in `geometry/out/moulds/`. Their volumes are listed in `moulds.md`.

- Print **each file twice**: the two halves are the same part.
- Print with the cavity facing up and no supports. Use 0.2 mm layers (0.12 mm for a smoother finish), 3 walls and 20% infill.
- To close the mould, turn one half over onto the other. The pegs on one diagonal drop into the sockets on the other diagonal.

| Priority | Mould | Why |
|---|---|---|
| Must | `pick_1` | Best all-rounder from the search |
| Must | `pick_4` | Strongest pick |
| Must | `ga2/B_narrowest_25mm/pick_1_mould_half.stl` | Backup lead if Nabat measures the **narrowest** width: 27.6 mm tip to tip, 25.7 mm at its narrowest, 5 lobes, 3.5 mm rounded rim |
| Must | `pick_1_rounded_rim` | Pick 1 with a 2.5 mm rounded outer rim. In the 3D simulation it never came to rest standing on its edge (pick 1 did in 25% of landings) |
| Must | `control_smooth_ring` | Pick 1 without the lobes. Shows what the lobes actually do |
| Must | `crush_test_disc` | Measures the mix's tensile strength |
| Optional | `pick_2`, `pick_3`, `pick_5` | The rest of the trade-off front |
| Optional | `waves/pick_1_waves_8x1.5mm_top_mould_half.stl` + `_bottom_mould_half.stl` | Your friend's up-and-down pie-crust waves on pick 1. **Print one of each** (the two halves differ). The simulation found no benefit; test it on the ramp and in the fan test to confirm |

## 2. Make the pods

1. Coat both cavities thinly with cooking oil, or dust them with cornflour.
2. Mix to a firm dough. It should hold its shape when squeezed and no water should come out. Write the recipe down.
3. Overfill each half slightly so the mix stands a little proud.
4. Close the mould, pegs into sockets. Press in a vice or clamp, or stand on a board laid over it, for 30 s.
5. Open the mould. Trim the thin rim of squeezed-out mix (the "flash") at the seam with a knife. Ease the pod out by flexing the mould. If it sticks, leave it to set in the mould for 30 to 60 minutes first.
6. Write a number on each pod in pencil. Dry in the shade for 48 to 72 h, turning it once. Weigh it each day: it's dry when the weight stops changing.
7. Make **20 pods of each "Must" design**. In the roll, fan and drop tests, also note whether each pod ends **flat or standing on its edge** (write `on edge` in `notes`), plus **10 crush-test discs per recipe** (strength varies a lot between pellets; the standard in pellet testing is 20, so 10 is the minimum for a usable average). For these mechanical tests, leave the seeds out or use cheap stand-in seeds of a similar size.

Use your pods like this, so most of them do more than one test:

| Pods | Tests, in order |
|---|---|
| 5 | Density → roll → fan → tumble → drying → soak (the soak destroys them) |
| 10 | Drop: 5 onto loose sand, 5 onto firm ground |
| 5 | Crush |

## 3. Tests (one datasheet row per pod per test)

Copy `test_data_template.csv` to `test_data.csv` and fill it in. Write the `design` name exactly as it
appears in the mould file name, for example `pick_1` or `control_smooth_ring`.

| Test | Method | Record |
|---|---|---|
| **density** | Weigh the dried pod. Measure the diameter tip to tip with calipers | `mass_dry_g`, `diameter_mm` |
| **roll** | Prop the 40 cm board so its top edge is **10 cm** above a hard floor. Stand the pod on its edge at the top, lobe down, and let go without pushing. It reaches the floor at about 1 m/s, the model's default. Measure from the foot of the ramp to where the pod's centre stops. Do 3 runs per pod, one row per run. If it falls flat on the ramp, redo it | `roll_cm`, `surface` = `floor` |
| **tumble** | Weigh 5 pods, put them in the lidded tub and shake at about 2 shakes per second for 5 minutes. Weigh them again. This mimics handling and loading into the drone | `mass_dry_g`, `mass_after_g` |
| **storage** (with the germination trays) | Coatings can lose their benefit over time (Patagonia, 2025). Make one batch of seeded pods 4 to 8 weeks before the tray test and store them dry, like real pods waiting for the January drop. Tray-test them next to freshly made pods | Germination counts in the tray datasheet (`research.md` §15) |
| **drying** | Rings and discs have a lot of surface, so they dry fast. Weigh the dry pod, wet it with 10 mL of water on a sand tray in the sun (or under a lamp), then weigh it every few hours. Record the hours until it is back within 5% of its dry weight. Run bare sand with the same water alongside as the comparison | `mass_dry_g`, `dry_hours` |
| **fan** | Lay the pod flat on a sand tray. Point a household fan on its highest setting at it from 30 cm for 2 minutes. Record `stayed`, `slid` or `rolled`. Note the fan and distance | `result`, `surface` = `sand` |
| **soak** | Put the pod on 2 cm of sand in a cup and pour 10 mL of water over it. Every 10 minutes, press a toothpick into the top gently. Record when it goes in 3 mm easily | `soften_min` |
| **crush** | Wear safety glasses. Stand the sample on its edge on the bathroom scale, between two flat offcuts of wood. Discs go on any edge. Pods go on a lobe tip, the way the model loads them. Press the top board down slowly and steadily, taking about 5 s to failure, while filming the scale's display. Note the highest reading before it cracks. For discs, also measure the diameter and thickness first | `peak_kg`, plus `diameter_mm` and `thickness_mm` for discs |
| **drop** | Get permission first. Clear the landing zone and post a spotter, with nobody underneath. Drop from **15 m** (about a 5th-floor balcony or stairwell). The rules only say *"UAE desert sites"* and *"variable … soil type"*, so test both desert extremes. **Loose sand:** the 20 cm sand tray, or a real dune. **Firm ground:** a gravel tray, or packed and dampened sand left to dry hard, standing in for gravel plains and crusted flats. Concrete isn't in the brief; use it only as an extra, harder-than-real check. If you can only reach a lower height, write the height in `notes`. If some pods carry real seeds, sow the seeds from dropped pods and from undropped pods side by side in a tray. A 2026 study found drop height affected germination, so check the seeds survive the impact, not just the pod. Grade each pod: `intact`, `cracked` (holds together but has a visible crack) or `broken` (in pieces, or more than 10% of its mass lost) On sand, also measure **how deep the pod sank**: lay a ruler across the sand and measure down to the pod's top surface (0 if it sits on the surface). Pods that end up partly buried do better (Flash Forest found embedded pods beat dropped ones) | `result`, `embed_mm`, `surface` = `sand` or `firm` (or `concrete` for the extra check) |

**Optional: measuring the real `--v0`.** Film some drops in slow motion with a tape measure lying in
view. Open the video in the free Tracker app (physlets.org/tracker) and measure how fast the pod is
moving just after its first bounce. A hand drop has no forward speed, so it gives the low end of the
range. A drone moving forward will add speed on top.

### Example rows

```csv
design,pod_id,test,surface,mass_dry_g,diameter_mm,thickness_mm,peak_kg,result,embed_mm,roll_cm,mass_after_g,soften_min,dry_hours,notes
pick_1,P1-03,density,,3.31,24.6,,,,,,,,,
pick_1,P1-03,roll,floor,,,,,,,14,,,,run 1
pick_1,P1-07,drop,firm,,,,,cracked,,,,,,15 m gravel tray
pick_1,P1-08,drop,sand,,,,,intact,9,,,,,15 m sand tray
pick_1,P1-04,drying,,3.30,,,,,,,,,31,
pick_1,P1-05,fan,sand,,,,,stayed,,,,,,fan on high 30 cm away
crush_test_disc,D-02,crush,,,29.4,9.8,6.2,,,,,,,
```

## 4. Analyse

```bash
uv run geometry/analyse_tests.py geometry/test_data.csv
```

This prints a summary for each design and writes `geometry/out/test_results.md`. The summary covers:
density, drop survival on each surface, roll distance, tumble loss, softening time and crush load.

It also checks the results against the model in three ways:
- **Crack load.** The crush discs give your mix's tensile strength. From that, the stress model predicts the load at which each pod shape should crack, shown next to what you measured.
- **Roll ranking.** A score shows whether the ramp test ranks the designs in the same order as the model: +1 means the same order, 0 means no relation.
- **Density.** It prints a command to re-run the search with your measured density.

### What to do with the results

| You see | Do this |
|---|---|
| Fewer than 4 out of 5 pods survive the drop onto sand | A serious problem: strengthen the mix (more clay or binder, date-palm fibre) or choose `pick_4`, then re-test |
| Pods survive sand but fewer than 4 out of 5 survive firm ground | Gravel plains and crusted flats may break them. Ask Nabat which ground the sites have before redesigning. If firm ground is likely, choose `pick_4` or strengthen the mix |
| Measured crack load is less than half the predicted load | The mix has air pockets or weak spots. Press harder, adjust the moisture, mix longer |
| Roll ranking score below +0.5 | The model's roll ranking doesn't hold on your surface. Choose the shape from the ramp data instead |
| Tumble loss above 2% | Pods will shed dust in the drone. Add binder (starch or CMC) or a coating |
| `pick_1` rolls about as far as `control_smooth_ring` | The lobes aren't working. Deepen them or reduce their number |
| Density far from 1.2 g/cm³ | Re-run the search with the printed command (about 9 minutes) |

Put the drop-survival percentages, the tumble loss and the strength figure on the
"Quality and Sustainability" slide. Put the roll and drop results on the "Integration with Nabat UAV" slide.
