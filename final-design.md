# TerraPod: final design document

Nabat TerraPod Challenge, Phase 1 proposal due **19 Nov 2026**. This is the single source of truth for
what we are building. Evidence lives in `research.md` and `prior-art.md`; models, moulds and bench tests in
`geometry/`.

| Part | Status |
|---|---|
| §2 Seed format and placement | **Final (v1, 5 Nov 2026)**. Counts and depths confirmed by tray tests |
| §3 Shape and morphology | **Chosen per mix (18 Nov)**: Mix A thin lobed ring, Mix B lobed disc (§3.0). Bench tests confirm |
| §4 Materials | Starting recipes, to be tested |
| §5 Manufacturing | Draft (press-mould method) |
| §6 Validation | Planned (`geometry/TEST_PROTOCOL.md` plus germination trays) |

---

## 0. Challenge rules (all official pages re-read 18 Nov 2026)

Sources: challengeon.atrc.ae/en/challenges/ntpc: brief, challenge statement, phases, FAQ, rules.

| Topic | What the rules say |
|---|---|
| Size | "2.5–3 cm diameter". **How it is measured is not stated** |
| Shape | Free: "spherical, oval / egg-shaped, cylindrical, disk-like, etc., as long as the dimension is within the specified limit" |
| Different shape per mix | **Not stated either way.** Rules ask for "seeds per species per seed-carrier" and say there are 2 mixes of 3 species |
| Number of designs or submissions | Not stated. The site shows a "Participate multiple times!" badge |
| Drop | Must survive "an expected drop height of 12–15 metres"; no landing surface given |
| Loading | Must work with Nabat's drone loading and survive pre-flight handling. No dispenser spec |
| Materials | Biodegradable, non-toxic, safe, no microplastics |
| Cost | "targeting ≤ AED 0.4" per carrier, with cost drivers and assumptions. Not stated whether seed cost counts |
| Habitat per mix | Not stated |
| **Phase 1** (deadline **19 Nov 2026**) | Participation form + **8 to 10-slide PDF deck, max 10 MB, in English**. Deck must cover: (1) team and experience; (2) composition (seeds per species per carrier), dimensions, preparation, deployment and UAV fit; (3) past deployment evidence and success rate, with references; (4) germination data vs. adjacent reference sites; (5) cost per carrier ≤ AED 0.4; (6) sustainability and biodegradability; (7) production capacity and scale over 5 years; (8) readiness (prototype or a credible plan to make one) |
| Phase 1 scoring | Called "weighted" but no weights are published: quality and sustainability, germination, cost, UAV integration, production and scalability. Proposals must also say how they improve on existing seed carriers |
| Phase 2 (Dec 2026) | Live short video pitch: rationale and development history, success rate, desert testing, team track record |
| Phase 3 (Jan 2027 to Q2 2027) | Validation materials due **1 Jan 2027**: ready-to-deploy carriers, or seed mix plus assembly instructions for ASPIRE (Nabat supplies seed). UAV field trial Jan to Feb 2027, 8 to 10 weeks, uncontrolled desert. Scored on germination **vs. adjacent reference areas** and on whether Nabat's UAV can deploy it |
| Prize and IP | US$50,000 and a possible partnership with Nabat. Winner keeps IP; sponsor gets a non-exclusive perpetual licence. Open-source parts must be disclosed. Entrants must be 18 or over |

---

## 1. The design in brief

**One pod family, two shapes, one per seed mix.** Both are solid, pressed and biodegradable, about 25 mm
across, with rounded lobes and a rounded rim that stop them rolling or standing on edge. Seeds sit in a
**thin seed skin on both flat faces**, so whichever way the pod lands a seeded face touches the soil. A
**seed-free core** of clay and date-palm fibre gives drop strength. Same recipe, same press, same seed skin;
only the mould differs (§3).

- **Mix A pod: thin lobed ring**, 6 mm thick, about 2.4 g. Its seeds are all small and sit in the skin, so
  it needs no thick core. The hole catches water and blown sand and lets pods stack on a rod.
- **Mix B pod: lobed disc, no hole**, 9 mm thick, about 3.8 g. The thickness gives the large *Calligonum*
  seed its pocket in the middle of the core; without the hole it is about **10× harder to crack**.

Mix A and Mix B pods can be dropped interleaved over the same ground, which gives all six species at a site
without putting both mixes in one pod (§7).

---

## 2. Seed format and placement: FINAL (v1, 5 Nov 2026)

### 2.1 Decision

**A solid ring with seeds in a thin seed skin on both flat faces; a seed-free core for strength; the
largest seed (*Calligonum*) in the middle of the core. No hollow capsule, and no seeds mixed through the
whole pod.**

```
   either face can land down
  ┌──────────────────────────────────────────┐
  │ ░ fine-sand dust (anti-ant, mould release) │  < 0.3 mm
  │ ● ● seed skin: low-clay mix + seeds        │  ~1.5 mm
  │ ▓▓▓ core: high-clay + date-palm fibre      │
  │ ▓▓▓      ◆ Calligonum pocket (mid-plane)   │  ~2.5–4 mm cover each side
  │ ▓▓▓ core                                   │
  │ ● ● seed skin: low-clay mix + seeds        │  ~1.5 mm
  │ ░ fine-sand dust                           │
  └──────────────────────────────────────────┘
```

### 2.2 Why

| Choice | Evidence (`prior-art.md`) |
|---|---|
| Seeds near the surface, not the centre | Small seeds near a pellet's edge came up **28 times better** than in the centre; with seeds in the centre, bare seed beat the pellets (Lieurance et al. 2024, §11.3, §13) |
| Seeds on the soil-facing face | Bottom of the pellet 70% emergence, bare seed 12 mm deep 57%, middle of the pellet 32% (Brown et al. 2023) |
| **Both** faces seeded | The pod is symmetric, so one seeded face is always down; the other is a backup if the pod flips or is buried |
| No hollow capsule | Encapsulation hurt germination in several studies; a hollow shell is weaker in a 15 m drop (§13) |
| Not mixed through | Wastes seed in the core and on the sun-side face; no species gets its best depth. Kept as a **test arm** |
| Thin skin, low clay | Thicker coats lower emergence; 10% clay beat 55% in the field; small seeds best at about 25% clay (§11.4, §11.5) |
| Fine-sand outer dust | A sand coat cut harvester-ant predation in 48 of 53 species (§9.7) |
| Prior art | Patented "seeds in a thin layer around an inert core" pills (US 5,389,115 / 5,623,781) |

### 2.3 Two pod types (one seed mix per pod)

| Pod | Species | Default seeds per pod (both faces) | Placement | Depth | Evidence |
|---|---|---|---|---|---|
| **Mix A** | *Eremobium aegyptiacum* | 20 (10 per face, clusters of about 5) | Skin, at the surface | 0 to 1 mm, pending the light/dark test | Desert mustards differ in light response; clusters push through crust |
| | *Cyperus conglomeratus* | 10 (5 per face) | Skin, at the surface | 0 mm | Germinates better in light |
| | *Stipagrostis plumosa* | 6 (3 per face), bristles removed | Bottom of the skin | 1 to 1.5 mm | Related grasses best at 0.5 to 2 cm |
| **Mix B** | *Panicum turgidum* | 6 (3 per face), **flat side outward** | Skin, at the surface | 0 mm | Emergence highest at the surface; flat side on wet soil |
| | *Haloxylon salicornicum* | 6 (3 per face), freshest seed | Bottom of the skin | 1 to 1.5 mm | Related *Haloxylon* best at 0.5 to 2 cm |
| | *Calligonum comosum* | 2, **scarified** | Core mid-plane, lying flat, side by side near the centre of the disc (in the ring version: inside two opposite lobes), ≥ 3 mm in from the rounded rim | About 2.5 to 4 mm cover each side | Prefers 2 to 4 cm (most a pod can give); large seeds cope best deep in a pellet |

- Seed mass per pod: about 13 mg (A) and 23 mg (B), under 1% of the pod.
- Counts aim for about 2 to 3 seedlings per pod at the 5 to 25% establishment typical worldwide; the tray
  trial tests ×0.5, ×1 and ×2.
- **Option if seed is costly:** put half the counts on each face.

### 2.4 Pre-treatment before pressing

| Species | Treatment |
|---|---|
| *Calligonum* | **Scarify** (sandpaper, nick or hot water; pick the method from the tray test, as no protocol exists for *C. comosum*) |
| *Stipagrostis* | Remove bristles (ask Nabat for cleaned seed); test a cold treatment |
| *Panicum*, *Stipagrostis* | Optional priming; check it survives pressing and storage |
| *Haloxylon* | Freshest seed, pressed as close to the drop as possible (loses viability fast) |
| All | Germination test of each seed batch before pressing |

---

## 3. Shape and morphology: one shape per mix (18 Nov 2026)

### 3.0 Mix-wise designs (current)

The earlier search gave both mixes the same 4 mm *Calligonum* pocket rule. Only Mix B carries *Calligonum*,
so the 3D genetic search (`geometry/ga2.py`) was re-run once per mix with its own rule:

- **Mix A:** pocket ≥ 3 mm, so the pod is ≥ 6 mm thick: a 1.5 mm seed skin on each face plus a ≥ 3 mm core.
- **Mix B:** pocket ≥ 4.5 mm, so ≥ 9 mm thick: a *Calligonum* seed about 3 mm thick (assumed; the brief gives
  2 to 6 mm) lying flat, with ≥ 3 mm of cover all round.

The Mix B winner was then also scored as a **lobed disc** (same outline, no hole). All designs below were
scored on the same 200 random 3D landings and the same edge-on squeeze (crush) test
(`geometry/mix_compare.py`, results in `geometry/out/mix_designs.md`).

**If "diameter" means tip to tip (main reading)**

| | Current lead (both mixes) | **Mix A: thin lobed ring** | Mix B ring | **Mix B: lobed disc** |
|---|---|---|---|---|
| Size, lobes | 25.0 mm, 4 | 25.1 mm, 4 | 25.0 mm, 4 | 25.0 mm, 4 |
| Thickness | 8.1 mm | **6.2 mm** | 9.0 mm | **9.0 mm** |
| Hole | 6 mm | 6 mm | 6 mm | **none** |
| Rounded rim | 2.5 mm | 3.4 mm | 3.5 mm | 3.5 mm |
| Mass (1.2 g/cm³ placeholder) | 3.17 g | **2.42 g** | 3.48 g | 3.79 g |
| Median travel after landing | 12.6 cm | **11.3 cm** | 12.9 cm | 13.5 cm |
| Rests on edge | 0.5% | 0.5% | 0.5% | 2.0% |
| Crush load (lead = 1, same mix) | 1.00 | 0.78 | 1.13 | **10.6** |
| Narrowest width | 20.4 mm | 20.5 mm | 20.3 mm | 20.3 mm |
| Mould | | `out/ga2_mixA/A_tip_to_tip/pick_1_mould_half.stl` | `out/ga2_mixB/A_tip_to_tip/pick_1_mould_half.stl` | `out/ga2_mixB/A_tip_to_tip/disc_version_mould_half.stl` |

**If the narrowest width must be ≥ 25 mm (backup reading):** 5 lobes, 27.4 to 27.6 mm tip to tip

| | Old backup (both mixes) | **Mix A ring** | Mix B ring | **Mix B disc** |
|---|---|---|---|---|
| Thickness | 7.9 mm | 6.1 mm | 9.0 mm (domed) | 9.0 mm (domed) |
| Mass | 3.95 g | 3.02 g | 4.14 g | 4.42 g |
| Median travel | 12.1 cm | 11.3 cm | 12.7 cm | 12.8 cm |
| Rests on edge | 1.5% | 0.5% | 1.0% | 1.0% |
| Crush load (lead = 1) | 1.44 | 1.11 | 1.36 | 3.47 |
| Mould (`out/…`) | `ga2/B_narrowest_25mm/pick_1_…` | `ga2_mixA/B_narrowest_25mm/pick_1_…` | `ga2_mixB/B_narrowest_25mm/pick_1_…` | `ga2_mixB/B_narrowest_25mm/disc_version_…` |

**Decision**

- **Mix A → thin lobed ring.** It is 24% lighter than the current lead, travels least, and keeps the hole for
  catching water and stacking on a rod. Its risk is strength: in the tip-to-tip version it cracks at 0.78× the
  lead's load. If the firm-ground drop test cracks it, fall back to the current lead (8 mm), which costs
  0.75 g more.
- **Mix B → lobed disc.** It is 9% heavier than the Mix B ring and travels about the same, but it is **10× harder
  to crack** (3.5× in the 5-lobe version). That matters for the heaviest, most valuable mix and for the firm
  gravel plains where *Haloxylon* grows. The *Calligonum* pocket moves to the centre of the disc, where the
  cover is deepest. What it gives up: no hole for catching water, and it stacks in a tube rather than on a rod.
- **Print all four** for the bench tests (both rings, the Mix B ring as the disc's control, the current lead
  as the reference). Then the drop and crush tests decide.
- **Material cost stays trivial:** at the placeholder AED 3/kg, every design is under AED 0.015.

**Model fix (18 Nov).** The squeeze model used to load a 5-lobe pod at only one of the two tips touching the
top board, which bent it and made every odd-lobe design look too weak. It now loads both tips evenly
(regression test in `test_pod_ga.py`; all 26 tests pass). The 4-lobe numbers and the genetic search (which
uses the impact model) did not change.

### 3.1 Earlier candidates (one shape for both mixes, 3 Nov)

| | Lead (if "diameter" = tip to tip) | Backup (if the narrowest width must be ≥ 25 mm) |
|---|---|---|
| Outline | 4 rounded lobes, 3 mm deep | 5 rounded lobes, 3 mm deep |
| Size | 25.0 mm tip to tip, 20.4 mm narrowest | 27.6 mm tip to tip, 25.7 mm narrowest |
| Thickness | 7.7 mm edge, 8.1 mm max | 7.9 mm edge |
| Hole | 6 mm | 6.1 mm |
| Rounded rim | 2.5 mm | 3.5 mm |
| Mass (1.2 g/cm³, placeholder) | 3.2 g | 4.0 g |
| Median travel after landing (3D) | 12.6 cm | 12.1 cm |
| Rests on edge | 0.5% | 1.5% |
| Impact stress (plain ring = 1) | 0.48 | 0.53 |
| Mould | `geometry/out/moulds/pick_1_rounded_rim_mould_half.stl` | `geometry/out/ga2/B_narrowest_25mm/pick_1_mould_half.stl` |

### 3.2 How we got here (`geometry/README.md`)

Crimped donut idea → ring and disc tie on 26 conditions → genetic search v1 (2D): **few deep, rounded
lobes beat pie-crust crimps** → 3D test: up-and-down waves add nothing on top of lobes; lobed rings rest
on edge in 25% of landings, **a rounded rim fixes it** → genetic search v2 (3D) confirms the lead and finds
the backup.

### 3.3 To revisit (Phase 2 work, after the bench tests)

- Lobe count, depth and profile: lobe depth sat at its 3 mm limit in both searches.
- Hole size: sat at its 6 mm minimum. Trade water catch and rod-stacking against strength (rings are much
  weaker than discs when squeezed).
- Thickness and doming versus the *Calligonum* pocket (cover sat at its 4 mm minimum) and the seed skin.
- How the seed skin (§2) and its lower-clay recipe change strength and the stress results.
- Rim rounding width (2.5 vs 3.5 mm).
- **Settled 18 Nov (§3.0), kept for the record. Mix A vs. Mix B (leaning, 7 Nov):** one design family, two versions. Same press method, lobes,
  rounded rim, seed skin and recipe; only dimensions change. Mix A: current lead (about 8 mm, 3.2 g).
  Mix B: thicker lobed ring (about 10 to 11 mm) or a lobed disc with no hole, for the *Calligonum* pocket
  and strength on gravel. Decide after Nabat says which mix goes to which ground, and after the bench tests.
- **Shape shortlist to compare next** (same 3D landing and stress tests, scored separately for Mix A and Mix B
  needs): (1) lobed ring + rounded rim (lead), (2) lobed disc, no hole, (3) bottom-weighted lobed dome
  (self-righting: always seed-side down), (4) cup/crater ring (holds water), (5) cone with a short tail
  (self-burying, the only route to *Calligonum*'s 2 to 4 cm depth; needs a sand model). Full catalogue of
  about 30 shapes in six families was reviewed on 5 Nov.
- Nabat's answers on diameter, dispenser and ground type.

---

## 4. Materials (starting recipes; all biodegradable, no microplastics)

| Layer | Starting recipe (by dry weight) | Why |
|---|---|---|
| **Sand dust** (outer) | Fine sand, dusted into the mould | Mould release and anti-ant coat |
| **Seed skin** | About 20% clay, 65% fine sand, 10% compost, 5% starch | Low clay is easy for shoots to break through |
| **Core** | About 50% clay, 40% sand, 2 to 3% date-palm fibre, 5% starch or CMC, ≤ 3% biochar | Drop strength; fibre stops cracks; little biochar, which weakens pods |
| Optional film | Thin starch–CMC spray after drying | A film coat gave +88% establishment in the Mu Us; may cut dust |

**Avoid:** PVAc binders, water crystals, and gypsum near *Cyperus* (salt-sensitive).

## 5. Manufacturing (press mould; both halves identical)

1. Dust both mould cavities with fine sand.
2. **Surface seeds** onto the sand in each half (Mix A: *Eremobium* clusters and *Cyperus*; Mix B:
   *Panicum*, flat side down).
3. Press about 1.5 mm of **skin mix** over them; add the deeper seeds (*Stipagrostis* or *Haloxylon*).
4. Fill each half with **core mix** to just proud of the parting line.
5. **Mix B only (disc mould, no centre pin):** press two scarified *Calligonum* seeds, lying flat and side
   by side, into the centre of the core in one half (≥ 3 mm from the rounded rim).
6. Close (pegs into sockets), press for 30 s, trim the seam, ease out, dry in the shade for 48 to 72 h.

These steps double as the **assembly instructions ASPIRE needs** if it builds the carriers (timeline,
Phase 3). At scale: a rotary tablet press with a centre pin and layered filling (see `research.md` §10).

## 6. Validation

| Test | Arms | Decides |
|---|---|---|
| Placement (trays) | Bare seed · ball mixed through · ring mixed through · **ring seed skin** | Whether the skin beats simpler options |
| *Eremobium* light (trays) | Surface vs. 2 mm cover | Its depth |
| Seed density (trays) | ×0.5 · ×1 · ×2 | Seeds per pod |
| *Calligonum* scarification (trays) | None · sandpaper · nick · hot water | Pre-treatment |
| Storage (trays) | Fresh vs. stored dry 4 to 8 weeks | Whether coatings or priming fade |
| Bench (`geometry/TEST_PROTOCOL.md`) | Density, roll, fan, tumble, drying, soak, crush, 15 m drop on sand and firm ground | Shape and recipe |

## 7. Open questions

- How Nabat measures diameter (picks the lead or the backup shape).
- **Both mixes in one pod: no (18 Nov).** The rules do not forbid it, but *Calligonum* needs a thick pod and the
  surface seeds a thin one; six species in one 25 mm spot crowd each other; the field trial supplies carriers
  "with the specified seed mix"; and every pod would carry about 36 mg of seed. Drop Mix A and Mix B pods
  interleaved instead.
- Whether seed cost counts toward AED 0.40.
- Drone dispenser type, ground type at the sites, irrigation.
- Final seeds-per-pod counts, after the density trial.

## 8. Decision log

| Date | Decision | Basis |
|---|---|---|
| 2 Nov 2026 | Ring with lobes, not a pie-crust crimp | Genetic search v1 (`geometry/README.md`) |
| 3 Nov 2026 | Pods land on desert ground, not concrete; drop-test on sand and firm ground | Challenge pages re-read |
| 3 Nov 2026 | Rounded outer rim (2.5 mm) | 3D test: lobed ring rested on edge in 25% of landings, 0% when rounded |
| 3 Nov 2026 | Lead + backup shape, depending on the diameter rule | Genetic search v2 |
| **5 Nov 2026** | **Seed skin on both faces, seed-free core, *Calligonum* in the core; one mix per pod** | §2 above |
| 7 Nov 2026 | One mix per pod (default). Leaning towards one design family with a Mix A and a Mix B version | Brief wording; habitat match; workload with 12 days left |
| 18 Nov 2026 | A different shape per mix is allowed: the rules leave shape free within 2.5 to 3 cm and do not require one design. Keep one family (same press, recipe, seed skin), with dimensions tuned per mix | §0 |
| 18 Nov 2026 | **Mix A: thin lobed ring (6 mm, 2.4 g). Mix B: lobed disc, no hole (9 mm, 3.8 g, about 10× harder to crack)**. Both mixes in one pod: rejected | Per-mix genetic search + `mix_compare.py` (§3.0); §7 |
| Next | Phase 1 deck (8 to 10 slides) from this doc; 5-shape comparison moves to Phase 2/3 work | §0 |
