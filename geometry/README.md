# TerraPod geometry search

A genetic algorithm (NSGA-II, via `pymoo`) that searches crimped-ring pod shapes and returns the
trade-off set: designs where no goal can improve without another getting worse. It narrows thousands
of shapes to five worth testing. It also makes press moulds for them and analyses your bench tests.
**It does not predict germination.** Only the tray and field tests can tell you that.

## Workflow

```bash
uv run geometry/pod_ga.py --out geometry/out          # 1. search: about 9 minutes
uv run geometry/moulds.py                             # 2. press moulds for the picks and the controls
# 3. print, press, dry and test the pods: TEST_PROTOCOL.md (2 to 3 days)
uv run geometry/analyse_tests.py geometry/test_data.csv   # 4. deck numbers, plus a check against the model
uv run geometry/pod_ga.py --density <measured> --cost-per-kg <quoted>   # 5. re-run with real numbers
uv run --python 3.11 geometry/waves3d.py            # 3D landing test: lobes vs up-and-down rim waves
uv run --python 3.11 --with pytest --with pymoo --with matplotlib --with "mujoco<3.3" pytest geometry -q   # all checks
```

`uv` installs each script's dependencies (numpy, scipy, matplotlib, pymoo, and MuJoCo for `waves3d.py`) on
its own, so your system Python is left alone. MuJoCo has no package for this Mac's Python 3.13, so
`waves3d.py` and the full test suite run on Python 3.11 (`--python 3.11`).

| File | Purpose |
|---|---|
| `pod_ga.py` | Shape model, physics models and the genetic search |
| `moulds.py` | Two-part press moulds. Both halves are the same part, aligned by pegs |
| `waves3d.py` | 3D rigid-body landing test (MuJoCo) of in-plane lobes vs. up-and-down rim waves; writes moulds for the best wavy variant |
| `analyse_tests.py` | Turns the bench-test datasheet into deck numbers and checks them against the model |
| `TEST_PROTOCOL.md` | How to make the pods and run the density, roll, tumble, soak, crush and drop tests |
| `test_data_template.csv` | Blank datasheet: copy it to `test_data.csv` |
| `test_pod_ga.py` | The physics checks |

## Outputs (`geometry/out/`)

| File | What it is |
|---|---|
| `summary.md` | The picked designs and two baselines (flat disc, plain ring), plus the assumptions used |
| `pareto.csv` | Every design in the trade-off set, with its shape settings and metrics. The `pick` column marks the five chosen |
| `pareto.png` | Mass vs. roll distance and mass vs. impact stress. Picks are circled |
| `picks.png` | Top view and cross-section of each pick, ready for a slide |
| `pick_N.stl` | The pod shape in mm. Use it to view the pod, or as a master for a silicone mould |
| `moulds/*_mould_half.stl` | Press moulds. **Print each one twice.** Pod volumes are in `moulds/moulds.md` |
| `test_results.md` | Written by `analyse_tests.py` |

## Shape settings (genes)

| Gene | Range | Meaning |
|---|---|---|
| `D` | 25 to 30 mm | Outer diameter, lobe tip to lobe tip (the brief's 2.5 to 3 cm) |
| `hole` | 6 to 14 mm | Centre hole diameter. The 6 mm minimum leaves room for a stacking rod and for the hole to catch water |
| `t_edge` | 4 to 12 mm | Thickness at the hole wall and at the outer wall |
| `dome` | 0 to 3 mm | How much each face bulges at mid-width (rounded top and bottom faces) |
| `n` | 3 to 24 | Number of crimp lobes |
| `a` | 0 to 3 mm | Crimp depth. 0 means a smooth ring |
| `p` | 0.5 to 3 | Crimp profile: below 1 gives broad valleys and pointed lobes, above 1 gives broad lobes and narrow valleys |

## Goals (all minimised)

| Goal | Model | Trust it for |
|---|---|---|
| `mass_g` | Exact volume × your density | Absolute values once the density is measured |
| `roll_m` | A rigid body rolling on edge over its convex outline. Each new contact point is treated as a perfectly plastic impact (the "rimless wheel" model from walking-robot research). Hard flat ground, no slip, no rolling resistance | **Ranking shapes only.** Sand stops every pod sooner. A result equal to the cap means "never stops on its own" |
| `stress_rel` | 2D plane-stress finite elements: the pod lands on its edge on a lobe tip and its own decelerating mass loads it. Thickness varies across the face, so doming counts. Peak tension is read outside 3 mm of the contact point, because that zone crushes rather than splits | **Ranking**, where 1.0 = a plain 30/10 × 10 mm ring. Covers edge-on landings only. Flat and tilted landings would need 3D FEM |

**Mesh note.** The search scores stress on a coarse mesh (`COARSE`, 360 × 8). That reads about 25%
low, but it ranks designs the same way as a finer mesh. All reported numbers are recomputed on `FINE`
(1440 × 32), which is about 5% below the fully converged value.

A solid disc gets no `stress_rel`. Its peak tension sits in the contact zone, which crushes rather
than splits, so the number would depend on the mesh. Compare rings with rings, and get the disc-vs-ring
answer from the crush and drop tests.

## Constraints

| Constraint | Default | Why | Flag |
|---|---|---|---|
| Calligonum pocket depth | ≥ 4 mm | Deepest point a seed can sit below every surface | `--cover-min` |
| Wall, hole to crimp valley | ≥ 4 mm | Press and mould filling, handling strength | `--wall-min` |
| Lobe tip radius | ≥ 1 mm | Sharp teeth chip in the tumble test | `--tip-r-min` |
| Valley radius | ≥ 0.5 mm | Press tooling | `--valley-r-min` |

The report also shows the **tip-over barrier**: how far the centre of mass must rise to flip a
flat-lying pod onto its edge (higher is steadier). It also shows **surface area ÷ volume**, which
tracks how fast a pod wets and dries.

## Placeholders to replace

1. **`--density`** (default 1.2 g/cm³). `analyse_tests.py` measures it and prints the re-run command.
2. **`--cost-per-kg`** (default AED 3/kg). Use real supplier quotes (`research.md` §11).
3. **`--v0`** (default 1 m/s). The rolling speed left after landing. The 10 cm ramp in the protocol
   gives about 1 m/s. For the real value, use slow-motion video of a drop.

Mass and cost scale with density. `roll_m` depends on `v0`. `stress_rel` doesn't depend on either.

## From bench tests to drop predictions (`analyse_tests.py`)

- **Mix strength.** The crush-test discs give the tensile strength: σ = 2P / (πDt).
- **Predicted crack load.** The model predicts the squeeze load at which each pod cracks:
  `strength ÷ squeeze_stress(pod)`. Put this next to the measured crack load to check the model.
- **Drop estimate.** The hardest edge-on stop each design survives, in g, and how much the ground must
  give for it to survive at 16 m/s. Loose desert sand gives roughly 10 to 30 mm, gravel or crusted ground only a few mm. The rules name no ground type: only *"UAE desert sites"* with *"variable … soil type"*. This
  assumes a constant deceleration and no local crushing, so it's on the cautious side. Your drop test
  is the real answer.
- **Roll ranking.** A Spearman rank score shows whether the ramp test ranks designs in the same order
  as the model.

## Physics checks (`test_pod_ga.py`)

- The volume and inertia of a plain ring match the textbook formulas.
- The pod mesh is closed, its faces point outward, and its volume matches the integrated volume.
- The mould mesh is closed, and its cavity holds half a pod to within 3%.
- The impact FEM matches the Brazilian disc formula to within 10%. The squeeze-test FEM matches it to within 15%.
- A rolling square tips over at exactly the speed theory predicts, and not at 5% below it.
- A smooth ring never stops rolling, while a deeply crimped one stops within a quarter of the cap.
- A flat ring's tip-over barrier matches √(R² + h²) − h.
- The test analysis gets density (with shrinkage), Brazilian strength, drop survival and tumble loss right.
- The drop estimate follows from strength, density and the impact stress.

## Findings so far (2 Nov 2026 run, default placeholders)

Design settings below are in mm except `n`.

| Design | D / hole / t_edge / dome / n / a | Mass | Roll | Stress vs plain ring |
|---|---|---|---|---|
| pick 1 (best all-rounder) | 25 / 6 / 7.7 / 0.2 / 4 lobes / 3 | 3.4 g | 0.11 m | 0.49 |
| pick 4 (strongest) | 25 / 6 / 10.8 / 0 / 3 lobes / 3 | 4.5 g | 0.40 m | 0.46 |
| pie-crust, 16 teeth × 1.5 mm | same body as pick 1 | 3.9 g | 0.31 m | 0.64 |
| smooth ring, same size as pick 1 | same body as pick 1 | 4.4 g | never stops | 0.65 |
| plain ring 30/10 × 10 | — | 7.5 g | never stops | 1.00 |

1. **Few deep lobes beat many small crimps.** Each lobe is a large "step", so the pod loses much more
   energy each time it rolls onto the next lobe. Pie-crust teeth roll about 3 times farther than pick 1,
   carry about 30% more peak stress, and are too sharp to pass the 1 mm anti-chipping limit.
2. **The lobes also cut stress.** Pick 1 has 25% less peak tension than the same body without lobes,
   and it's lighter.
3. **Rings are much weaker than discs in a squeeze.** The model says a ring cracks at roughly a tenth
   of the load that cracks a solid disc of the same mix. A thin-ring hand calculation agrees on the
   size of the effect. A ring fails by bending at the hole; a disc has no hole to bend around. The pods land on
   desert ground, not concrete, so the risk is firm gravel or crusted ground, not loose sand. If firm-ground
   drops fail, make the pod thicker (pick 4) or use a stronger mix before giving up on the hole.
4. **The search is pressing against the limits.** `D` sits at 25 mm, `hole` at 6 mm and `a` at 3 mm in
   every pick, and the Calligonum pocket depth sits at its 4 mm minimum. The results reflect those
   choices, so revisit them with Nabat's dispenser and size tolerance in hand. A 3-lobe pod measures
   about 22 mm across its flat sides, and pick 1 measures **20.4 mm** at its narrowest with calipers (`ga2.narrowest_width_mm`), so check both against the brief's 2.5 to 3 cm. `ga2.py` scenario B designs for the strict reading.

## Up-and-down rim waves vs. lobes: 3D landing test (`waves3d.py`, 3 Nov 2026)

MuJoCo 3D rigid-body simulation: 200 identical random landings per design (random orientation, sideways
0.5 to 2 m/s, downward 0.5 to 2 m/s, spin 0 to 30 rad/s), hard flat ground. Full table:
`out/waves/results.md`; chart: `out/waves/distances.png`.

| Design | Median travel | 90th percentile | Ends standing on edge | Mass |
|---|---|---|---|---|
| **Pick 1, rounded rim 2.5 mm** | **12.5 cm** | **33 cm** | **0%** | 3.16 g |
| Pick 1 (4 lobes) | 14.2 cm | 37 cm | 25% | 3.38 g |
| Pick 1 + 8 waves × 1.5 mm | 14.3 cm | 38 cm | 25% | 3.38 g |
| Pick 1 + 4 waves × 1.5 mm | 18.2 cm | 42 cm | 24% | 3.38 g |
| Smooth ring + 8 waves × 1.5 mm (pie crust) | 31.6 cm | 246 cm | 0% (still rolling at 4 s: 44%) | 4.42 g |
| 16 in-plane teeth × 1.5 mm | 27.0 cm | 92 cm | 8% | 3.88 g |
| Smooth ring | 105 cm | 341 cm | 0% (still rolling at 4 s: 67%) | 4.42 g |

1. **Waves help a smooth ring a lot** (median 105 cm down to 32 cm) but **add nothing on top of the
   lobes** (14.2 cm vs. 14.3 to 18.2 cm). The lobes already do the job.
2. **Waves cost soil contact.** A wavy pod lying flat rests on its wave crests, leaving a gap of up to
   twice the wave height (3 mm for 1.5 mm waves) under the seeded face at the rim.
3. **New finding: pick 1 ends standing on its edge in 25% of landings.** The flat stretch of rim
   between two lobe tips is a stable base, so neither seeded face touches the soil. **A 2.5 mm rounded
   outer rim removes this completely (0%)**, also travels least, saves 0.2 g, and doesn't weaken the pod
   (FEM, approximate: peak stress 0.478 vs. 0.491, because the peak sits at the hole, not the rim).
4. **New lead design: pick 1 with a 2.5 mm rounded rim** (`out/moulds/pick_1_rounded_rim_mould_half.stl`,
   print twice). Pick 1 stays as the control that shows the rounding works; the wavy moulds
   (`out/waves/*_top_` and `*_bottom_mould_half.stl`, one of each) are optional.

ponytail: rigid pod on hard ground with Coulomb friction, no sand, no breakage. It ranks shapes; the
ramp, fan and drop tests decide.

## Genetic search v2 (`ga2.py`, 3 Nov 2026)

8 genes (v1's 7 plus `rim`, the rounded-rim width). Objectives: mass, **median 3D travel over the same 60
random landings** (MuJoCo), impact stress (rim-aware FEM). New rules: rests on edge in at most 5% of
landings, no hooking (hole narrower than the ring's thickness and wall). Two readings of "2.5–3 cm
diameter": **A** = tip to tip, **B** = narrowest caliper width ≥ 25 mm too. Picks and the current lead
re-scored on 200 landings with the fine-mesh FEM. Results: `out/ga2/A_tip_to_tip/` and `out/ga2/B_narrowest_25mm/`.

| Design | Tip to tip | Narrowest | Lobes | Rim | Mass | Median travel | Ends on edge | Stress |
|---|---|---|---|---|---|---|---|---|
| **Current lead** (v1 pick 1 + 2.5 mm rim) | 25.0 | 20.4 | 4 | 2.5 | **3.17 g** | 12.6 cm | 0.5% | 0.48 |
| A pick 1 | 25.5 | 20.9 | 4 | 3.1 | 3.37 g | 12.8 cm | 2.5% | 0.47 |
| **B pick 1** (strict width) | 27.6 | **25.7** | 5 | 3.5 | 3.95 g | **12.1 cm** | 1.5% | 0.53 |
| B pick 4 | 29.2 | 26.2 | 6 | 3.4 | 4.76 g | 12.2 cm | 2.0% | 0.58 |

1. **Scenario A confirms the current lead.** The search converged on the same family (4 lobes about 3 mm
   deep, 6 mm hole, about 8 mm thick, 3 mm rounded rim) and found nothing that beats the lead on mass and
   travel together. Its best alternative is 6% heavier for 2% less stress.
2. **Scenario B: if Nabat measures the narrowest width, the lead fails (20.4 mm).** Use **B pick 1**:
   27.6 mm tip to tip, 5 lobes, 3.5 mm rim, 25.7 mm at its narrowest. It's 25% heavier (still under
   AED 0.02 of material at the placeholder price), travels slightly less, and carries 10% more stress.
3. **Limits still binding:** lobe depth (3 mm), hole (6 mm) and the Calligonum pocket (4 mm) sit at their
   bounds again, and B pushes the rim to its 3.5 mm maximum. Loosening those is the next lever.
4. **Runtime:** 4 h 48 min, not the 20 min estimated. (An earlier note here blamed an idle worker pool;
   that was wrong. `time` hadn't counted the workers' CPU.) Profiling found the real causes:
   - Random early designs that are thick and domed **rock like a lens** for the full 4 simulated seconds.
     In one design, 31 of 60 landings were still moving at the time limit.
   - Uneven job lengths cap the 10-worker speed-up at about 5.5×.

   **Fixed:** in search mode a landing stops at 1 m or 2 s, and a pod still moving at 2 s counts as
   rolled away (1 m). That's a fair penalty, since rocking for 2 s is bad behaviour. The final check
   of the picks keeps the full, uncapped 4 s simulation. Scoring now takes 3.2 s per design instead of
   5.5 s, so a full run is about 50 minutes. The results above came from the slower exact run and stand.

## Mix-wise designs (18 Nov 2026)

Each seed mix gets its own pocket rule: Mix A has no *Calligonum*, so `--cover-min 3.0` (≥ 6 mm thick: two
1.5 mm seed skins plus a ≥ 3 mm core); Mix B `--cover-min 4.5` (≥ 9 mm: a ~3 mm *Calligonum* seed with
≥ 3 mm of cover). `mix_compare.py` then scores each Mix B pick as a lobed disc too (same outline, no hole),
all on the same 200 landings and the same squeeze test. Results: `out/mix_designs.md`; decision in
`../final-design.md` §3.0.

```bash
uv run --python 3.11 geometry/ga2.py --cover-min 3.0 --out geometry/out/ga2_mixA   # ~25 min on 10 cores
uv run --python 3.11 geometry/ga2.py --cover-min 4.5 --out geometry/out/ga2_mixB   # ~25 min (75 min on a busy machine)
uv run --python 3.11 geometry/mix_compare.py --shrink 0.05 --dried-min 26         # ~1.5 min; also writes out/print/
```

| Tip to tip | Thick | Hole | Mass | Median travel | On edge | Crush load (lead = 1) |
|---|---|---|---|---|---|---|
| Current lead | 8.1 mm | 6 mm | 3.17 g | 12.6 cm | 0.5% | 1.00 |
| **Mix A ring** | 6.2 mm | 6 mm | 2.42 g | 11.3 cm | 0.5% | 0.78 |
| Mix B ring | 9.0 mm | 6 mm | 3.48 g | 12.9 cm | 0.5% | 1.13 |
| **Mix B disc** | 9.0 mm | none | 3.79 g | 13.5 cm | 2.0% | **10.6** |

**Squeeze-model fix.** `squeeze_stress` used to load the 3 highest mesh nodes. A pod with an odd number of
lobes touches the top board at two tips, so the load landed unevenly on them, bent the pod, and made it look
far too weak (a 5-lobe disc came out barely stronger than the same ring). `board_nodes` now loads every node
within 0.01 mm of each board, evenly. The 4-lobe results and the genetic search (impact model) are unchanged;
the old 5-lobe backup's crush load rises to 1.44× the lead's.

**Print size.** The searched designs sit at exactly 25.0 mm and clay shrinks as it dries, so `mix_compare.py`
also writes `out/print/`: the final designs scaled evenly to dry at ≥ 26 mm tip to tip, with moulds enlarged
by `--shrink` (placeholder 5%; measure one pressed pod and re-run). Table: `out/print/print.md`.
