# Nabat TerraPod Challenge: research brief

Researched 23 Oct 2026. Deadline **Thu 19 Nov 2026** (27 days away).

How to read this:
- **Sourced** facts have a link.
- Lines marked **(our analysis)** are my working: calculations, design reasoning, guesses to test. They are not from a source.
- Lines marked **(to verify)** are things I believe but could not confirm.

## Contents

1. [The challenge in one page](#1-the-challenge-in-one-page)
2. [Who is behind it](#2-who-is-behind-it)
3. [What exactly they ask for](#3-what-exactly-they-ask-for)
4. [How it is judged](#4-how-it-is-judged)
5. [The basics: why seeding the desert is hard](#5-the-basics-why-seeding-the-desert-is-hard)
6. [The six species](#6-the-six-species)
7. [What already exists](#7-what-already-exists)
8. [The physics: drop, size, weight](#8-the-physics-drop-size-weight)
9. [Materials](#9-materials)
10. [How carriers are made](#10-how-carriers-are-made)
11. [Cost: AED 0.40 per carrier](#11-cost-aed-040-per-carrier)
12. [Possible solutions](#12-possible-solutions)
13. [Questions to tackle](#13-questions-to-tackle)
14. [Questions to ask the organisers](#14-questions-to-ask-the-organisers)
15. [Plan to 19 November](#15-plan-to-19-november)
16. [Glossary](#16-glossary)
17. [Sources](#17-sources)

---

## 1. The challenge in one page

**The question**, word for word:

> How might we design a scalable, low-cost seed-carrier that can be deployed by drone to reliably establish vegetation in the desert and arid landscapes of the UAE?

The more detailed version in the challenge statement:

> How might we develop a low-cost UAV-deployable seed carrier that accommodates multiple native UAE seeds of varying sizes and that significantly enhances vegetation establishment in desert and arid environments?

**In plain words:** design a small biodegradable "pod" that holds seeds of native UAE desert plants. A drone drops it from 12 to 15 m, and it has to help those seeds sprout better than seeds that land on their own.

| Requirement | Value |
|---|---|
| Size | **2.5 to 3 cm** across. Any shape: sphere, egg, cylinder, disc |
| Drop | Survives **12 to 15 m** from Nabat's drone |
| Handling | Must not break down during pre-flight handling or loading |
| Cost | **≤ AED 0.40 per carrier** (about US$0.11) |
| Materials | Biodegradable, non-toxic, safe, **no microplastics** |
| Seeds | **2 mixes × 3 native species**. You choose how many seeds of each species go in one carrier |
| Must beat | Germination in **"adjacent reference areas"** (nearby ground used for comparison) |
| Stresses to overcome | Extreme heat, wind, water scarcity, poor and saline soils, seed predation, **seed dormancy** |

| Phase | When | What |
|---|---|---|
| 1. Proposal | now to **19 Nov 2026** | Form + **8 to 10 slide PDF, max 10 MB** |
| 2. Video pitch | Dec 2026 | Short live video pitch to the semi-finalists' evaluators |
| 3. Validation | send carriers by **1 Jan 2027**; field test Jan to Feb 2027 | Nabat drops them in real desert for **8 to 10 weeks** |
| Review | Mar 2027 | Expert review |
| Winner | Q2 2027 | **US$50,000** (about AED 184,000) + a possible commercial partnership with Nabat |

**Fallback if you can't make the pods yourselves** (timeline page, Phase 3, verified 3 Nov 2026): *"Where a finalist cannot supply ready-to-deploy seed carriers (containing the seeds), they must instead provide their seed mix along with clear instructions for ASPIRE to assemble the carriers. In the latter case, Nabat will provide the seeds."* So a clear, reproducible recipe and assembly method is itself a deliverable. The pressed-mould method (`geometry/moulds.py`) suits this well.

Source: [challenge brief](https://challengeon.atrc.ae/en/challenges/ntpc), [challenge statement](https://challengeon.atrc.ae/en/challenges/ntpc/pages/challenge-statement?lang=en), [phases](https://challengeon.atrc.ae/en/challenges/ntpc/pages/timeline?lang=en).

**Eligibility:** 18 or over. Teams are allowed: "Where a team or entity participates, the person submitting the Project Proposal represents that they have authority to act on behalf of that team." **Team members cannot change without written consent**, so settle the team before submitting. You must also declare any other funding the solution has received. ([Rules](https://challengeon.atrc.ae/en/challenges/ntpc/agreements?lang=en), clauses 3 to 5)

---

## 2. Who is behind it

| Name | What it is | Role here |
|---|---|---|
| **ATRC** (Advanced Technology Research Council) | Abu Dhabi government body set up by Law No. 14 of 2020, which runs the emirate's advanced research | Organiser |
| **ASPIRE** | ATRC's "innovation acceleration arm". Runs grand challenges such as the US$5M MBZIRC robotics challenge, and works with XPRIZE | Runs the challenge |
| **VentureOne** | ATRC's commercialisation arm, which turns research into companies | Launched Nabat |
| **TII** (Technology Innovation Institute) | ATRC's applied research arm | Built the technology behind Nabat |
| **Nabat** (Nabat A I Technologies LLC SPC) | Nature-tech company in Masdar City, Abu Dhabi (Accelerator 2 Building) | Challenge partner. Its drone does the field test, and it may partner with the winner |
| **ChallengeON** | ATRC's challenge platform | Where you register and submit |
| **Agorize** | French company that runs the platform | Sends emails, runs the chat |
| **EAD** (Environment Agency – Abu Dhabi) | Abu Dhabi's environment regulator | Nabat's partner on mangroves, and runs its own drone desert seeding |

### Nabat in more detail

- **Launched December 2024** by VentureOne. It started by restoring mangroves with drones, AI and seeding equipment, working with EAD on "thousands of hectares" over seven years. ([TII](https://www.tii.ae/news/nabat-new-abu-dhabi-climate-tech-venture-use-ai-and-robotics-restore-mangroves-and-boost), [The National](https://www.thenationalnews.com/climate/2024/12/10/uae-to-harness-ai-to-help-protect-crucial-mangroves-as-global-efforts-falter/))
- **How it works:** AI reads satellite images and other data to choose sites, then drones seed them. Its estimated seed success rate on mangroves was **about 30%**, which they called conservative because it was still a pilot. ([The National](https://www.thenationalnews.com/climate/2024/12/10/uae-to-harness-ai-to-help-protect-crucial-mangroves-as-global-efforts-falter/))
- **NabatOS** is its platform: one pipeline from mapping and choosing sites, through autonomous aerial seeding, to satellite and drone monitoring "so every restoration program can demonstrate that restoration worked". It has now expanded from mangroves to "coastal, marine, and dryland ecosystems". ([About the partner](https://challengeon.atrc.ae/en/challenges/ntpc/pages/about-challenge-partners?lang=en), [nabat.ai](https://nabat.ai/))
- **Why they're running this (our analysis):** Nabat has the drone and the monitoring. What it lacks is a pod that works in dry desert, which is very different from mangrove mud. Your carrier is the missing piece of their desert product. They'll want something they can make by the million and track from the air.

---

## 3. What exactly they ask for

### 3.1 Technical requirements (from the challenge statement, section 03)

- **Planting conditions:** "suitable for variable ranges of temperature, humidity, solar intensity, salinity, soil type, and irrigation requirement"
- **Target species:** "2 seed mixes with 3 species per mix… participants to determine the ratio of species per mix"
- **Environmental compliance:** "biodegradable, non-toxic, and safe (no microplastics); meeting desert requirements"
- **Drone fit:** "2.5–3 cm diameter, compatible with the Nabat UAV platform"
- **Loading and handling:** "must not degrade during pre-flight handling or loading on the UAV"
- **Impact resistance:** "structural integrity during aerial deployment… at an expected drop height of 12–15 metres"
- **Readiness:** prototype-stage is fine, but you need "a credible path to producing a ready-to-deploy seed-carrier in time for field validation in January and February 2027"
- They also say proposals "should clearly articulate how their approach improves on existing seed-carrier mechanisms". **A plain seed ball isn't enough. You have to say what's better.**

### 3.2 What the 8 to 10 slide deck must cover

1. Team overview and relevant experience (who you are, and whether you can deliver)
2. Carrier composition (**seeds per species per carrier**), dimensions, how it's made, how it's deployed, drone fit
3. **Historical evidence of seed-carrier deployment and success rate, with external references**
4. **Germination performance data (vs adjacent reference sites)**
5. Indicative cost per carrier (≤ AED 0.40), with **key cost drivers and pricing assumptions**
6. Sustainability and biodegradability (non-toxic, safe, no microplastics)
7. **Production capacity and scalability over the next 5 years**
8. Readiness (prototype status, or a credible plan to build one)

You must also disclose any open-source parts (Rules clause 39). Write everything in English.

**(our analysis)** Items 3 and 4 are hard for a new student team, because you have no field history. The honest way through:
- For item 3, cite published evidence for the *type* of carrier you're building (sections 7 and 12).
- For item 4, run your own small germination test before 19 Nov. Compare your carrier with bare seeds of the same species in the same sand, so the bare seeds act as your "reference". Say clearly that it's a lab or greenhouse test, not a field test.

### 3.3 The species table they give

| Mix | Species | Family | Life form | Dormancy (their table) | Seed size | ~1000-seed weight |
|---|---|---|---|---|---|---|
| A | *Eremobium aegyptiacum* | Brassicaceae (mustard) | Annual ephemeral | None / physiological | 0.5 to 1 mm | 0.18 g |
| A | *Cyperus conglomeratus* | Cyperaceae (sedge) | Perennial sedge | Minimal / epigeic | 1 to 2 mm | 0.42 g |
| A | *Stipagrostis plumosa* | Poaceae (grass) | Perennial grass | Shallow physiological | 2 to 3 mm (caryopsis) | 0.85 g |
| B | *Panicum turgidum* | Poaceae (grass) | Perennial grass | Minimal | 2 to 3 mm | 1.52 g |
| B | *Calligonum comosum* | Polygonaceae (buckwheat) | Perennial shrub | **Physical (hard seed coat)** | 2 to 6 mm | 2.98 g |
| B | *Haloxylon salicornicum* | Amaranthaceae | Perennial shrub | Short physiological | 2 to 3 mm | 1.24 g |

**(our analysis)** Read the last column carefully. An *Eremobium* seed weighs **0.18 mg**, so 1,000 of them weigh less than a paperclip. Tiny seeds carry tiny food reserves, so the seedling can only push up through a few millimetres. **A tiny seed buried in the middle of a 3 cm ball will never come up.** This one fact shapes the whole design: small seeds near the surface, bigger seeds deeper. See section 12.

**(our analysis)** The two mixes probably match two habitats. Mix A looks like sand dune and sandy plain (*Cyperus conglomeratus* is a known dune binder, *Stipagrostis* is a sand grass). Mix B looks like gravel and sandy plains with shrubs. (to verify) Ask Nabat which sites each mix is for, because the soil decides a lot.

---

## 4. How it is judged

| Phase | Criteria |
|---|---|
| **1. Proposal** | Five weighted criteria (the weights aren't published): **Overall quality and sustainability · Germination effectiveness · Cost effectiveness · Integration with Nabat UAV · Production and scalability** |
| **2. Video** | **Experience and track record:** why this solution, how it was developed, success rate so far, whether it has been tested in desert conditions. **Team competence and confidence:** do evaluators believe you can deliver? |
| **3. Field** | **Germination effectiveness:** "a germination rate higher than that in adjacent reference areas". **Integration with Nabat UAV:** could their drone deploy it? |

Other things to know:
- They may use **AI tools to screen and score** proposals, though a human makes the final call (Rules clause 18). **(our analysis)** So use the exact words from their criteria as slide headings, and put clear numbers on each slide. That helps a human reviewer and a scoring tool alike.
- **"Participate multiple times!"** appears on the brief. (to verify) You may be able to submit more than one design.
- The judging panel doesn't have to pick a winner if no entry is good enough (clause 14).
- **(our analysis)** The field test lasts 8 to 10 weeks and measures **germination**, not survival a year later. Research shows seed balls reliably improve early emergence even when they don't improve long-term survival (section 7.1). So the thing being measured is the thing pods are best at. Still, claim survival benefits honestly, since the brief also asks about "early-stage survival".

### IP and money

- **You keep ownership of your IP.** The winner grants Nabat and ATRC a perpetual, non-exclusive, royalty-free licence. A discussion about an *exclusive* licence "may be a prerequisite for prize disbursement". ([Challenge statement §06](https://challengeon.atrc.ae/en/challenges/ntpc/pages/challenge-statement?lang=en), Rules 30 to 38)
- Every participant gives a free licence for evaluation and "internal review and discussion regarding potential collaboration" (clause 32). The organisers may also independently develop similar ideas (clause 44). **(our analysis)** Mark anything truly secret as "Confidential" (clause 42). Better still, don't include what you're not willing to share.
- Data from submissions can be used to train their AI tools (clause 40).
- You must attend scheduled events, at least one team member each time (clause 17).

---

## 5. The basics: why seeding the desert is hard

### 5.1 The UAE climate

- **Rain:** about **120 mm a year or less**, irregular. Most falls **December to May**. ([EAD soils chapter](https://www.researchgate.net/publication/259174728_Soils_of_Abu_Dhabi_Emirate), [UAE desertification paper](https://www.researchgate.net/publication/259178629_Soil_and_water_management_for_combating_desertification_-_towards_implementation_of_the_United_Nations_Convention_to_Combat_Desertification_from_the_UAE_perspectives))
- **Heat:** summer often reaches 45 to 50 °C, the yearly average is 28 °C, and winter can drop to 3 °C. Evaporation is higher than rainfall. (same sources)
- **Soils:** often alkaline (pH above 8), saline, sodic and low in nutrients. ([Open Agriculture Journal](https://openagriculturejournal.com/VOLUME/18/ELOCATOR/e18743315279696/FULLTEXT/))
- **When the desert grows:** after good rains it blooms in spring. In 2026 rain was "exceptional" and EAD opened camel-grazing season early, on 22 April. ([The National](https://www.thenationalnews.com/news/uae/2026/05/01/the-rains-have-fallen-the-deserts-in-bloom-and-camel-grazing-season-can-begin-a-month-early/))
- **(our analysis)** A January to February test falls in the cool, rainy window, which is good. But if no rain falls during those 8 to 10 weeks, nothing germinates, carrier or no carrier. Ask whether they'll irrigate (section 14).

### 5.2 The six barriers your carrier has to beat

| Barrier | What happens to a bare seed | What a carrier can do |
|---|---|---|
| **Dormancy** | Seed is alive but won't sprout until conditions are right | Pre-treat the seed (priming, scarification, after-ripening), and keep it moist long enough |
| **Water scarcity** | One small rain wets the seed, it starts, then dries out and dies | Hold water near the seed (clay, organic matter, natural hydrogels), and shade the soil underneath |
| **Heat and sun** | Surface sand can be far hotter than the air | Light colour, shade, mass that buffers temperature |
| **Wind** | Light seeds blow away or get buried too deep under drifting sand | A heavy, flat shape that doesn't roll. Anchoring |
| **Salinity** | Salt stops some species germinating (*Cyperus conglomeratus* germination "greatly reduced in 25 mM NaCl and completely inhibited in 50 mM") | A low-salt pocket of material around the seed |
| **Predation** | Ants, rodents and birds eat seeds. In one grassland study, up to 87% of seed vanished in 3 days, and ants took up to 55% | A physical shell, plus deterrents (capsaicin, neem, activated carbon) |
| **Poor soil** | No nutrients, no helpful microbes | Compost, biochar, mycorrhizal fungi or helpful bacteria |

Sources: [Cyperus germination thesis, UAEU](https://scholarworks.uaeu.ac.ae/all_theses/651/), [savanna seed predation](https://www.sciencedirect.com/science/article/pii/S025462991631105X), [desert seed removal](https://www.sciencedirect.com/science/article/abs/pii/S014019631200242X).

### 5.3 Germination vs emergence vs establishment

These three words get mixed up, and the judges care about the difference:
- **Germination:** the seed sprouts (a root comes out).
- **Emergence:** the shoot comes up above the soil, or above the carrier.
- **Establishment:** the seedling survives and anchors, usually counted weeks to months later.

Phase 3 says "germination rate". **(to verify)** In the field they'll almost certainly be counting **emerged seedlings**, since nobody digs up pods to look. Ask how and when they count.

### 5.4 Burial depth

- Seeds lying on the surface of sand rarely germinate, and the few that do can't anchor their roots. Shallow burial is best: for one desert shrub, 0.2 to 0.5 cm; for a dune grass, 1 cm. Emergence drops as depth goes from 2 to 12 cm. Larger seeds come up from deeper. ([Frontiers in Plant Science 2018](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2018.01167/full))
- *Calligonum*: across ten species, deeper burial meant lower and slower emergence. Most seedlings came from 2 to 4 cm, and the deepest emergence was 12 cm. ([Ren et al. 2002, AGRIS](https://agris.fao.org/search/en/records/65de28d67c7033e84be9f184))
- **(our analysis)** A pod sitting on the surface acts like "seed on the surface" unless it breaks down, sinks into the sand, or the seed is right at its skin. How the pod meets the soil matters as much as what's in it.

---

## 6. The six species

Local names: **Arta** = *Calligonum* (EAD calls it "Fire Bush", *C. polygonoides*; *C. comosum* is usually treated as a subspecies of it), **Rimth** = *Haloxylon salicornicum*, **Thamam** = *Panicum turgidum*. ([EAD via Zawya](https://www.zawya.com/en/special-coverage/zawya-green/environment-agency-abu-dhabi-disperses-65mln-native-seeds-using-drones-slc62u2s), [AGBI](https://www.agbi.com/sustainability/2023/12/abu-dhabi-uses-drones-and-ai-to-reseed-desert-land/))

All three Mix B species are already used in EAD's drone seeding, so there's local experience to cite.

### Mix A

**Eremobium aegyptiacum** (annual, mustard family)
- The smallest seed in either mix (0.18 g per 1,000). It's an ephemeral: it sprouts after rain and finishes its life quickly.
- The evidence on dormancy conflicts. One study found no dormancy-regulating chemical broke its dormancy ([J Plant Growth Regul 2016](https://link.springer.com/article/10.1007/s00344-016-9640-z)). A camel-rangeland study listed it among the best germinators, sprouting across a wide range of temperatures ([ResearchGate](https://www.researchgate.net/publication/368673377_Improving_seed_germination_of_native_species_for_camel_rangeland_restoration_effects_of_cold_stratification_and_temperature)).
- **(our analysis)** It needs to sit at or very near the pod surface. It's the species most likely to show quick emergence in an 8 to 10 week test.

**Cyperus conglomeratus** (perennial sedge)
- A dune-binding sedge. Its germination is "greatly reduced in 25 mM NaCl and completely inhibited in 50 mM NaCl". Fusicoccin, GA3 (a plant hormone) and kinetin "completely alleviated salinity induced dormancy". ([UAEU thesis](https://scholarworks.uaeu.ac.ae/all_theses/651/))
- **(our analysis)** It's very salt-sensitive, so it benefits most from a low-salt, moist pocket. GA3 is a natural plant hormone, but check that it counts as "non-toxic, safe" for the judges.

**Stipagrostis plumosa** (perennial grass)
- Responded positively to **cold stratification**, which points to physiological dormancy. ([camel rangeland study](https://www.researchgate.net/publication/368673377_Improving_seed_germination_of_native_species_for_camel_rangeland_restoration_effects_of_cold_stratification_and_temperature))
- Temperature and water potential strongly affect germination in *Stipagrostis*, and the seeds need "quite specific conditions". ([ScienceDirect, hydrothermal time](https://www.sciencedirect.com/science/article/abs/pii/S0048969725009830))
- **(our analysis)** The name "plumosa" means feathery. Its seeds have plume-like awns (bristles) that catch the wind, which makes them hard to pack into a pod by machine. Ask whether Nabat supplies them cleaned, with awns removed.

### Mix B

**Panicum turgidum** (perennial grass, "Thamam")
- The challenge table says dormancy is "Minimal". But a Kuwaiti study found it needs **after-ripening** (dry storage before it will germinate) and has deeper dormancy than *Pennisetum divisum*. ([Biologia 2025](https://link.springer.com/article/10.1007/s11756-025-02023-1)) **(to verify)** Ask how old Nabat's seed lot is.
- It germinates much better when its **flat side touches wet soil**, not its round side. ([Gul et al., halophyte.org](https://www.halophyte.org/pdfs/drkhan_pdfs/182.pdf))
- Salinity tolerance has been tested on UAE seed with NaCl and KCl from 25 to 400 mM. ([Seed Science & Technology 2004](https://www.ingentaconnect.com/content/ista/sst/2004/00000032/00000003/art00024))

**Calligonum comosum** (shrub, "Arta")
- It has **physical dormancy** (a hard seed coat), so water can't get in until the coat is broken.
- It produces yellow and red fruits, and seed colour affected germination in the lab (red seeds did best in dark and heat), though not in the shade house. ([Bhatt et al. 2019](https://zuscholars.zu.ac.ae/works/1279))
- Germination fell as salt stress rose and stopped above 100 mmol/L. ([J King Saud Univ Sci 2024](https://doaj.org/article/9122314ea7354d2b843e0b4f452ceeae))
- In a Kuwaiti greenhouse, seedlings came up in 30 to 55 days.
- **(our analysis)** Physical dormancy is broken by **scarification**: scratching, sanding or nicking the coat, a hot-water soak, or an acid treatment. Without it, you may see nearly nothing within 8 to 10 weeks. This could be your biggest single win. I found no study that tests scarification on *C. comosum* specifically, so test it yourselves.

**Haloxylon salicornicum** (shrub, "Rimth")
- No dormancy break needed. Kuwaiti seeds "could germinate at very high percentages immediately".
- **Temperature-sensitive:** best below 20 °C, "severely retarded" above 30 °C. It germinates less under light-dark cycles and in full darkness, and is sensitive to NaCl. ([El-Keblawy & Al-Shamsi 2008, via review](https://link.springer.com/rwe/10.1007/978-3-030-17854-3_45-1))
- **(our analysis)** Cool January suits it. A dark pod centre may slow it, so place it near the surface.
- (to verify) *Haloxylon* seeds are often said to lose viability quickly in storage. If so, pod shelf life matters. Ask how long pods will sit between making and dropping.

### Summary: where each seed goes (our analysis)

| Species | Seed | Key need | Place in pod | Pre-treatment to test |
|---|---|---|---|---|
| Eremobium | Tiny | Light, shallow | Outer skin | None / GA3 |
| Cyperus | Small | Low salt, moisture | Outer layer | Rinse; possibly GA3 |
| Stipagrostis | Medium, awned | Cool and moist cue | Middle | Cold stratification; remove awns |
| Panicum | Medium, flat side | Flat side on wet soil, after-ripened | Outer layer, on the flat face of a disc | After-ripening check; priming |
| Calligonum | Large, hard coat | Scarification | Deeper (big reserves) | Scarify |
| Haloxylon | Medium | Cool, near the surface | Outer layer | None |

---

## 7. What already exists

### 7.1 Seed balls: what the research says

The evidence is **mixed but useful.** Pods often help seeds emerge; they don't reliably help plants survive long-term.

- **Johnstone et al. 2026, Restoration Ecology** (arid US): they tested sphere, disc and cube shapes, with different clay amounts and with nutrients or soil inoculants. "Seedballs initially enhanced plant emergence but not establishment", with **no significant difference by shape, clay, nutrients or inoculant**. Over two years, the balls neither helped nor hurt native cover. ([Wiley](https://onlinelibrary.wiley.com/doi/10.1111/rec.70303)) **This is the most relevant paper. Read it in full.**
- **Organic-enriched seed balls in arid land, Plant and Soil 2026:** with a 10% organic amendment, germination was 48 to 92% across four species, against under 10% for direct sowing. ([Springer](https://link.springer.com/article/10.1007/s11104-026-08530-7))
- **Brazil landfill 2026:** **60% clay** balls gave the best germination, survival and growth. ([Springer](https://link.springer.com/article/10.1007/s11355-026-00736-2))
- ***Vachellia nilotica*:** **2 cm** thickness worked best. A thicker 2.5 cm ball with more watering grew worse. ([ResearchGate review](https://www.researchgate.net/publication/384848426_Seedball_Technology_Facets_and_Prospects_for_Restoration_of_Degraded_Lands)) **(our analysis)** That's a warning for a 2.5 to 3 cm pod: thickness can hurt.
- **New Zealand 2025:** tree species germinated poorly in balls. Some failures were down to seed handling, not the ball. ([NZ J Botany](https://www.tandfonline.com/doi/full/10.1080/0028825X.2024.2432314))
- **Habitat Authority 2011:** seed balls gave germination where broadcast seed gave none, but took a lot of labour. ([PDF](https://www.habitatauthority.org/fc/studies/Seed-Ball-Experiment-Report-January-2011.pdf))
- **Review of pelleting for arid land:** pellets don't greatly reduce germination and may help, but results vary widely. ([ResearchGate](https://www.researchgate.net/publication/336152944_Review_of_seed_pelletizing_strategies_for_arid_land_restoration))
- **Seedballs Kenya:** seed inside **charcoal dust** with nutritious binders, to deter birds, rodents and insects. Dropped from the air in Kenya. Wikipedia notes there's "no published data" showing aerial seed balls work. ([Seedballs Kenya](https://www.globallandscapesforum.org/wp-content/uploads/2018/09/Seedballs-Kenya-Overview-GLF-2018-compressed.pdf), [Wikipedia](https://en.wikipedia.org/wiki/Aerial_seeding))

### 7.2 Seed enhancement technologies (SETs)

- **Extruded pellets** (Matthew Madsen's group, Brigham Young University): seeds mixed into a dough and pushed through a die like pasta, then cut into short cylinders. Pellets raised sagebrush emergence 3.1-fold at 10 mm depth. They've been used in the field with topsoil and *Triodia* (spinifex) in Australian dryland. ([Madsen et al.](https://www.researchgate.net/publication/313991670_Emerging_seed_enhancement_technologies_for_overcoming_barriers_to_restoration), [PLOS ONE 2018](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0204380), [Alfonzetti 2023](https://onlinelibrary.wiley.com/doi/10.1111/rec.13857), [Harshani 2024](https://onlinelibrary.wiley.com/doi/full/10.1111/emr.12600))
- **Activated carbon pellets** protect seeds from herbicide and "show promise" in dryland restoration. ([Swartz 2026](https://onlinelibrary.wiley.com/doi/10.1111/rec.70316))
- A **global review** says SETs still need work: the best additives and their amounts are unknown. ([Science of the Total Environment](https://www.sciencedirect.com/science/article/abs/pii/S0048969721041681))

### 7.3 Drone seeding companies

| Company | Where | Approach |
|---|---|---|
| **Dendra Systems** | UK / Australia | Drones that map then seed. **Ran EAD's arid trial in Al Dhafra.** Each drone can carry 53 species and covers 100+ football fields a day |
| **AirSeed** | Australia | Seed pods fired from drones. 40,000 pods a day (an older figure; it now claims up to 250,000) |
| **Flash Forest** | Canada | Patented seed pods plus drones. 300,000 pods, 19 species, 13 sites in its 2021 pilot |
| **Mast Reforestation** (formerly DroneSeed) | USA | Heavy-lift drone swarms over burned forest |
| **Terra Drone Arabia** | Saudi Arabia | Says it drops "biodegradable seed pods" with seeds, nutrients and moisture-retaining material (vendor claim) |

Sources: [Mongabay](https://news.mongabay.com/2023/07/new-tree-tech-cutting-edge-drones-give-reforestation-a-helping-hand/), [DroneLife](https://dronelife.com/2022/08/26/planting-trees-with-drones-airseed-delivers-seed-pods-for-drone-reforestation-initiative/), [AirSeed](https://www.airseedtech.com/), [Flash Forest](https://www.flashforest.com/), [Terra Drone Arabia](https://terra-drone.com.sa/drone-applications-for-environmental-from-desertification-to-disaster-response/).

A 2024 review of drone seeding says the fastest reported rate is 120 pods a minute, and that **companies rarely disclose their technology, so their claims are hard to check**. ([Australian Forestry](https://www.tandfonline.com/doi/full/10.1080/00049158.2024.2343516))

### 7.4 The UAE track record

- **EAD + Dendra + ADQ:** arid drone trial in Al Dhafra, using native species chosen by soil, salinity and ground cover: Ghaf, Samar, Arta, Shoua, Raghal, Thamam. Over **6.5 million seeds on 320 hectares** in nature reserves, including Fire Bush and Rimth in dune areas. A plan to drop **10 million** native seeds. ([Abu Dhabi Media Office](https://www.mediaoffice.abudhabi/en/environment/environment-agency-abu-dhabi-and-adq-partner-with-dendra-to-enhance-terrestrial-and-coastal-restoration-through-advanced-technologies/), [Zawya](https://www.zawya.com/en/special-coverage/zawya-green/environment-agency-abu-dhabi-disperses-65mln-native-seeds-using-drones-slc62u2s), [Gulf News](https://gulfnews.com/uae/environment/how-abu-dhabi-plans-to-revive-its-deserts-with-10-million-seeds-1.500628192))
- **No germination results for the desert trial have been published** as far as I could find. The often-quoted **48% success rate is for mangroves**, not desert. ([EAD](https://www.ead.gov.ae/en/Media-Centre/News/0-plants-one-million-mangrove), [The National](https://www.thenationalnews.com/climate/environment/2023/01/12/drones-scatter-one-million-mangrove-seeds-in-abu-dhabi/))
- EAD's projects are described as dropping **seed bags**, not pods. ([AGBI](https://www.agbi.com/sustainability/2023/12/abu-dhabi-uses-drones-and-ai-to-reseed-desert-land/))
- **Saudi Arabia:** drones are seeding royal reserves (for example, 300,000 sidr seeds). ([Middle East AI News](https://www.middleeastainews.com/p/can-drones-reforest-the-gulf-region))

### 7.5 The benchmark to know: self-burying seed carriers

- **Carnegie Mellon (Luo, Yao et al.), *Nature* 2023:** a wooden carrier with tails modelled on *Erodium* seeds. When wet, the tails twist and **drill the seed into the ground**. Dropped by drone, it had an **80% drilling success rate on flat land** after two wet-dry cycles. ([Nature](https://www.nature.com/articles/s41586-022-05656-3), [CNN](https://www.cnn.com/world/powered-by-rain-seed-carrier-reforest-remote-areas-scn-climate-spc-intl/index.html), [Interesting Engineering](https://interestingengineering.com/innovation/bioinspired-seed-carrier))
- **(our analysis)** Judges will probably know this paper. It isn't built for the 2.5 to 3 cm, AED 0.40, two-mix brief, but it shows that "getting the seed into the soil" is a recognised problem. *Stipagrostis* seeds have similar twisting awns of their own, which is a nice local link to mention.

---

## 8. The physics: drop, size, weight

**(our analysis)** I calculated these myself for a sphere (drag coefficient 0.47, air density 1.2 kg/m³). Shapes other than spheres will differ a little.

| Diameter | Density | Mass | Carriers per kg | Speed at ground (15 m) | Impact energy (15 m) |
|---|---|---|---|---|---|
| 2.5 cm | 0.8 g/cm³ (porous) | 6.5 g | 153 | 14.8 m/s (53 km/h) | 0.7 J |
| 2.5 cm | 1.6 g/cm³ (dense clay) | 13.1 g | 76 | 15.9 m/s | 1.7 J |
| 3.0 cm | 0.8 g/cm³ | 11.3 g | 88 | 15.1 m/s | 1.3 J |
| 3.0 cm | 1.6 g/cm³ | 22.6 g | 44 | 16.1 m/s (58 km/h) | 2.9 J |

What this tells you:
1. **Air drag barely helps.** Pods this heavy fall almost as if there were no air, landing at about 14 to 16 m/s. Plan for full impact.
2. **Weight trades off against the drone.** A lighter pod means more pods per flight and less impact energy, but it blows around more once it lands. Ask Nabat for the maximum pod weight and the drone's payload.
3. **Hard ground is the worst case.** Sand absorbs impact. Gravel plains and crusted ground don't.
4. **The drone is also moving forwards**, which adds sideways speed. The pod may bounce and roll, which is one argument for a disc or egg shape over a sphere.
5. **How to test it cheaply:** drop pods from 15 m (about a 5-storey building or stairwell, with permission and somebody keeping the area below clear) onto concrete and onto sand. Record the percentage that stay whole and the seeds lost. Also do a "tumble test": shake pods in a box for a few minutes to simulate handling and loading.

**Hardness vs germination (our analysis):** a pod hard enough to survive concrete may be too hard for roots to escape, or may block water. Possible fixes: a hard outer shell that softens when wet, a weak point built in, or a design where seeds sit at the surface.

---

## 9. Materials

All of them must be **biodegradable, non-toxic, with no microplastics.** That rules out the usual polyacrylamide-type "water crystals" used in gardening. Fossil-based superabsorbents are a known source of microplastics, and the EU bans non-biodegradable ones from 2028. ([HEC / A&B Smart Materials](https://www.hec.edu/en/dare/innovation-entrepreneurship/ab-smart-materials-replacing-microplastic-biodegradable-alternatives))

| Role | Options | Notes |
|---|---|---|
| **Body / bulk** | Clay (bentonite, kaolin, local red clay), sand, local topsoil, compost | Cheap. 60% clay was best in one study. Clay forms a hard protective shell when dry |
| **Binder** | Starch, gum arabic, clay alone, alginate, CMC (carboxymethyl cellulose), molasses | Starch and CMC are cheap. Alginate forms gels with calcium |
| **Water holding** | Bentonite, compost, cellulose or starch hydrogels, cocopeat, date-palm fibre | Pure hydrogels struggle in dry soil. Cross-linked starch/CMC did better ([Nature Sci Rep 2025](https://www.nature.com/articles/s41598-025-30594-1)) |
| **Soil improver** | Biochar (including **date-palm biochar**), compost | The UAE has about **42 million date palms**. Date-palm biochar has been tested as a sandy-soil conditioner in the UAE ([MRF](https://mrforum.com/product/9781644900178-11/), [review](https://link.springer.com/article/10.1007/s12517-022-11123-0)). A strong local, circular-economy story |
| **Protection** | Charcoal dust, activated carbon, chilli (capsaicin), neem oil | Coated seeds cut rodent eating by 47 to 50%, and even a **blank coating** gave 99% avoidance when food was plentiful. Methyl-nonyl-ketone hurt germination ([USDA FS](https://research.fs.usda.gov/treesearch/61381)) |
| **Antimicrobial film** | Chitosan | Strengthens the film, and slowed water and nutrient release without harming germination ([PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11818308/)) |
| **Biology** | Mycorrhizal fungi (AMF), helpful bacteria (PGPR) | AMF from Arabian desert plants boosted *Prosopis cineraria* growth ([Symbiosis 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8933382/)). Low commercial doses were ineffective in a prairie study, and fungus-to-plant matching matters |
| **Dormancy breaking** | Scarification (physical), priming (water or salt solution), GA3 | Done to the seed before it goes into the pod |

**(our analysis)** "Natural" isn't automatically "biodegradable and non-toxic in the desert." Biodegradation is very slow in dry sand. Write down how each material breaks down, and avoid anything that leaves residue.

---

## 10. How carriers are made

| Method | How | Good for | Downsides |
|---|---|---|---|
| **Hand rolling** | Mix dough, roll balls by hand | Prototypes now | Slow, uneven. Can't claim scale |
| **Pan / drum pelletiser** | A rotating pan coats seeds layer by layer, like making sweets | Layered designs, cheap at scale | Hard to put different seeds in exact places |
| **Extrusion** (Madsen) | Dough pushed through a die and cut | Cylinders, high throughput, proven for dryland | Seeds spread evenly through the dough, so tiny seeds end up deep |
| **Compression / tablet press** | Powder pressed in a mould, like a pill | Exact size, discs, very fast, cheap per unit, seeds can be placed in the top layer | Needs the right powder mix. Pressed tablets may be very hard |
| **Moulding** | Wet mix pressed into silicone moulds | Prototype discs and eggs now | Slow drying |
| **Alginate dripping** | Drops of alginate into a calcium bath form beads | Lab gel beads | Expensive, hard to get to 3 cm, weak |

**(our analysis)** For the deck: prototype by **moulding** now, and propose a **tablet press or pan pelletiser** for scale. Both are standard industrial machines, which makes the "5-year production capacity" slide believable. For example: "One rotary tablet press makes N per hour, so M million per year." Get real machine figures from a supplier.

---

## 11. Cost: AED 0.40 per carrier

- AED 0.40 ≈ **US$0.11**. In practice that's a few fils per gram of material.
- **(our analysis)** Typical cost lines:
  1. Bulk materials (clay, compost, biochar): cheap per kg, but you use 7 to 23 g per pod.
  2. Binder and additives: small amounts, but some (alginate, chitosan, AMF) are expensive.
  3. Seeds: (to verify) is seed cost inside the AED 0.40? Phase 3 says "Nabat will provide the seeds" if you can't. Ask.
  4. Labour and machines: worked out per pod from machine throughput.
  5. Drying, packing, shipping.
- **What to put on the slide:** a table of material, grams per pod, price per kg (from a real quote), and fils per pod, plus a labour/machine line and a total. They specifically ask for "key cost drivers and the assumptions behind the pricing".
- **(our analysis)** A lighter pod costs less to make *and* lets the drone carry more. That's a cost argument for the 2.5 cm size and a porous body.

---

## 12. Possible solutions

**(our analysis)** These are concepts for you to choose from and test, ordered from easiest to most ambitious. You can combine them.

### A. Improved clay–compost seed ball (baseline)
Clay + compost + date-palm biochar, about 60% clay, with a charcoal or chilli outer coat.
- **For:** cheap, proven, easy to prototype this week.
- **Against:** the brief asks you to improve on existing carriers, and on its own this *is* the existing carrier. Use it as your control.

### B. Layered pod: each seed at its own depth
- **Skin (top 1 to 3 mm):** tiny seeds (*Eremobium*, *Cyperus*) stuck on with a starch or gum film, plus a deterrent.
- **Middle:** medium seeds (*Stipagrostis*, *Panicum*, *Haloxylon*).
- **Core:** a water store (bentonite, cellulose/starch gel, fibre), plus the big scarified *Calligonum* seed.
- **Why it's better:** it fixes the tiny-seed-buried-too-deep problem directly, and it answers the "seeds of varying sizes" wording in the question.

### C. Flat disc ("TerraPod tablet")
- A 3 cm by about 1 cm disc, pressed. Flat means it **doesn't roll**, sits flat on the sand, and shades the soil under it.
- Seeds are in the face that touches the ground (for *Panicum*, flat side down), so they're in contact with moist soil.
- Made on a tablet press, which is a fast, believable route to scale.
- Weakness: it may land the wrong way up. Consider seeds on both faces, or a weighted side.

### D. Water-harvesting pod
- Hydrophilic outer layer and a water-holding core, so it **captures a small rain or heavy dew** and holds it against the seeds for days.
- It acts as a mini **"nurse" microsite**: shade, mulch, and less salt.
- Test: how many days a wetted pod stays moist in hot sun, compared with bare sand.

### E. Pod that breaks down on cue
- Hard when dry (survives the drop and handling), **slumps into a mound when wet**, which half-buries the seeds at the right shallow depth.
- **(our analysis)** This may be the cleverest answer to "survive 15 m *and* release seeds." Test it by soaking pods, then timing how long they take to collapse.

### F. Self-anchoring pod (most ambitious)
- Uses awns or a twisting tail, like *Stipagrostis* or the CMU carrier, to work into the soil.
- **Against:** hard to make, hard to fit within 3 cm and AED 0.40 in 4 weeks. Mention it as a future direction.

### Recommended shortlist (our analysis)
Build **A as the control**, and **B + C + E as your entry**: a pressed disc, layered so tiny seeds are on the skin, that softens when wet. Then test all of them side by side (section 15).

### How many seeds per pod (our analysis)
They leave it to you. Things to weigh:
- More seeds means a better chance at least one comes up. But seedlings in one spot compete, and seed supply costs money.
- Tiny seeds weigh almost nothing: 20 *Eremobium* seeds weigh 3.6 mg.
- **Test it:** for example, 3 densities (low, medium, high) for each mix. Count emergence per pod and per seed.

---

## 13. Questions to tackle

Your team's research to-do list. Each one should produce a number or a decision for the deck.

**Biology**
1. For each species, what's the germination rate of bare seed in your test sand at about 20 °C? (This is your reference.)
2. Does scarifying *Calligonum* raise germination in 2 to 4 weeks? Which method: sandpaper, a nick, or hot water?
3. Does cold stratification help *Stipagrostis*? For how many days?
4. Does priming (soaking then drying) speed up emergence, and does it survive being packed into a pod?
5. How deep can each species' seedling push through *pod material* and still come up?
6. Do helpful microbes (AMF, PGPR) add anything in 8 to 10 weeks, or only later? (Johnstone 2026 found no benefit from inoculant.)

**Physical**
7. What's the survival rate after a 15 m drop onto concrete and onto sand, for each recipe?
8. What happens after 5 minutes of tumbling? (handling and loading)
9. How long does a wetted pod stay moist in sun, compared with bare sand?
10. How long does a pod take to soften once wet? Does it ever break down completely?
11. What's the pod's weight and how many fit in 1 kg?
12. Does a disc roll less than a sphere when dropped at an angle, or in wind (test with a fan)?

**Protection**
13. Do ants take seeds from the pod compared with bare seed? (A simple outdoor test: count seeds left after 24 to 48 hours.)
14. Does chilli or charcoal coating harm germination?

**Commercial**
15. What does each material cost per kg in the UAE (real quotes)?
16. What's the total cost per pod, and which line costs the most?
17. What can one machine produce per hour or year, and what does that mean for 5-year capacity?
18. Where do you get the six species' seeds for testing *before* Phase 3? (EAD? Nabat? Local seed suppliers?) If you can't get them in time, which commercially available seeds of similar size can you test with, and how do you explain that honestly?

**Strategy**
19. What's your one-line "this improves on existing seed balls because…"?
20. What can you honestly say for "historical evidence" and "success rate" as a new team?

---

## 14. Questions to ask the organisers

Use the platform chat ("dedicated chat with the Admins"). Answers may change your design.

1. **Team registration:** the page says "Individual participation". How do we register a team of two? Who submits?
2. **Seeds:** can participants get the six species' seeds for testing before 19 Nov? Is seed cost included in the AED 0.40?
3. **Size rule (decides between our two final designs):** "Our carrier is a ring with rounded lobes. Is the 2.5 to 3 cm diameter measured across the widest point (lobe tip to lobe tip), or must the narrowest width also be at least 2.5 cm? Is there a thickness limit?" If tip to tip, use `pick_1_rounded_rim` (25 mm, 20.4 mm at its narrowest). If narrowest, use `ga2/B_narrowest_25mm` pick 1 (27.6 mm, 25.7 mm at its narrowest).
4. **Drone:** what's Nabat's dispenser mechanism? Maximum pod mass? Tolerance on the 2.5 to 3 cm size? Flight speed when dropping? Do pods need to flow freely through a hopper?
5. **Sites:** what soil (dune sand, sandy plain, gravel)? Which mix goes where?
6. **Water:** will the validation sites be irrigated, or rely on rain?
7. **Measurement:** how is "germination" counted (emergence per pod? per seed?), and in which week? How are "adjacent reference areas" set up: bare seed, or natural vegetation?
8. **Volume:** how many pods do finalists supply by 1 Jan 2027?
9. **Mixes:** must each pod carry one mix (3 species), or can we split species across pods?
10. **Multiple entries:** does "Participate multiple times!" mean we can submit more than one design?
11. **Additives:** are plant hormones (GA3) and microbial inoculants acceptable under "non-toxic, safe"?
12. **Storage:** how long do pods sit between delivery and the drop, and in what conditions (heat, humidity)?

---

## 15. Plan to 19 November

**(our analysis)** Germination tests take 2 to 4 weeks, so **start them this week**. Everything else can fit around them.

| Week | Dates | Do |
|---|---|---|
| 1 | 23 to 29 Oct | Register (both of you), send the organiser questions, get seeds or stand-ins, buy materials. Make the first batches: A (control), B, C and E, 3 seed densities. **Start the germination test** (pods vs bare seed, in trays of local sand, near a window or in a cheap grow setup). Start pre-treatment tests (*Calligonum* scarification, *Stipagrostis* cold). |
| 2 | 30 Oct to 5 Nov | Drop tests (15 m, concrete and sand), tumble test, water-holding test, softening test. Get material quotes. Read Johnstone 2026 and Madsen in full. |
| 3 | 6 to 12 Nov | Count germination (photos every 2 to 3 days). Ant test. Choose the final recipe. Work out cost per pod and production capacity. |
| 4 | 13 to 18 Nov | Build the deck (8 to 10 slides, under 10 MB). Get a friend to review it. **Submit on 18 Nov**, a day early. |

**A possible deck outline (10 slides):**
1. Title + one-line promise
2. Team, and why you can deliver
3. The problem, in numbers (rain, heat, predation, dormancy)
4. The design: cut-away diagram showing where each seed sits, size, shape, weight
5. How it's made, and how it fits the drone
6. Evidence: literature on carrier types + your test results vs bare seed (your "reference")
7. Drop and handling results
8. Cost per pod table + cost drivers
9. Sustainability: every material and how it breaks down
10. 5-year scale-up + readiness + plan to 1 Jan 2027

---

## 16. Glossary

| Term | Meaning |
|---|---|
| **Seed carrier / seed pod / seed ball / seed bomb** | A small object that holds seeds and protects them until they sprout |
| **Seed pellet** | A seed (or seeds) covered in material to make a bigger, uniform shape |
| **Seed coating** | A thin layer on a single seed (thinner than a pellet) |
| **Encapsulation** | Enclosing seeds inside a material |
| **Extrusion** | Pushing dough through a shaped hole to make continuous pellets |
| **SET** (seed enhancement technology) | Any treatment that improves seed performance: coating, pelleting, priming |
| **UAV** | Unmanned aerial vehicle (a drone) |
| **BVLOS** | Beyond visual line of sight: flying a drone the pilot can't see |
| **Payload** | The weight a drone can carry |
| **Hopper / dispenser** | The container and mechanism that holds and releases pods |
| **Terminal velocity** | The top speed of a falling object, when air drag balances gravity |
| **Germination** | A seed sprouting; the root comes out |
| **Emergence** | The shoot appearing above the surface |
| **Establishment** | A seedling surviving and rooting over weeks to months |
| **Germination rate / percentage** | Share of seeds that sprout |
| **Mean germination time** | Average days to sprout |
| **Viability** | Whether a seed is alive (tested with a tetrazolium dye test) |
| **Dormancy** | A live seed that won't sprout until certain conditions are met |
| **Physiological dormancy** | Dormancy caused by the embryo's chemistry. Broken by time, cold, warmth or hormones |
| **Physical dormancy** | A hard, waterproof seed coat. Broken by scarification |
| **Scarification** | Scratching, nicking or softening the seed coat so water can get in |
| **Stratification** | Holding moist seeds cold (or warm) for a while to break dormancy |
| **After-ripening** | Dry storage after harvest that slowly breaks dormancy |
| **Priming** | Soaking seeds so they start germinating, then drying them, so they sprout faster later |
| **Imbibition** | A seed soaking up water, the first step of germination |
| **GA3** (gibberellic acid) | A plant hormone that can break physiological dormancy |
| **Seedbank** | Dormant seeds stored in the soil |
| **1000-seed weight** | Weight of 1,000 seeds, the standard measure of seed size |
| **Caryopsis** | The "seed" of a grass (technically a fruit) |
| **Awn** | A bristle on a grass seed. Some twist with moisture |
| **Epigeal (epigeic)** | Germination where the seed leaves are pushed above ground |
| **Ephemeral / annual** | A plant that lives one season, often sprouting right after rain |
| **Perennial** | A plant that lives for years |
| **Halophyte** | A salt-tolerant plant |
| **Psammophyte** | A plant adapted to sand |
| **Dune binder** | A plant whose roots hold sand in place |
| **Salinity / EC** | Saltiness, measured as electrical conductivity (mS/m, dS/m) |
| **mM NaCl** | Salt concentration in millimoles per litre (seawater is about 600 mM) |
| **Sodic soil** | Soil high in sodium, which crusts and drains badly |
| **Hydrogel / SAP** (superabsorbent polymer) | A material that soaks up many times its weight in water. Many are plastic and banned here |
| **Biochar** | Charcoal made for soil, to hold water and nutrients |
| **AMF** (arbuscular mycorrhizal fungi) | Fungi that live on roots and help plants take up water and nutrients |
| **PGPR** | Plant-growth-promoting rhizobacteria: helpful root bacteria |
| **Granivore** | An animal that eats seeds (ants, rodents, birds) |
| **Nurse microsite** | A small sheltered spot (under a shrub or a pod) where seedlings survive better |
| **Reference area / control** | Nearby ground without your treatment, used for comparison |
| **Biodegradable** | Broken down by living things into natural substances |
| **Microplastics** | Plastic fragments under 5 mm that persist in the environment |
| **TRL** (technology readiness level) | A 1 to 9 scale from idea to proven product |
| **Non-exclusive licence** | Permission to use your IP, while you can still license it to others |

---

## 17. Sources

**Challenge**
- [Brief](https://challengeon.atrc.ae/en/challenges/ntpc) · [Challenge statement](https://challengeon.atrc.ae/en/challenges/ntpc/pages/challenge-statement?lang=en) · [Phases and evaluation](https://challengeon.atrc.ae/en/challenges/ntpc/pages/timeline?lang=en) · [FAQ](https://challengeon.atrc.ae/en/challenges/ntpc/pages/faq?lang=en) · [Rules](https://challengeon.atrc.ae/en/challenges/ntpc/agreements?lang=en) · [About ASPIRE](https://challengeon.atrc.ae/en/challenges/ntpc/pages/about-organizers?lang=en) · [About Nabat](https://challengeon.atrc.ae/en/challenges/ntpc/pages/about-challenge-partners?lang=en)

**Organisations**
- [TII: Nabat launch](https://www.tii.ae/news/nabat-new-abu-dhabi-climate-tech-venture-use-ai-and-robotics-restore-mangroves-and-boost) · [The National: Nabat mangroves](https://www.thenationalnews.com/climate/2024/12/10/uae-to-harness-ai-to-help-protect-crucial-mangroves-as-global-efforts-falter/) · [nabat.ai](https://nabat.ai/) · [Middle East AI News](https://www.middleeastainews.com/p/atrc-ai-robotics-venture-nabat) · [WAM: ASPIRE launch](https://www.wam.ae/en/article/hszrbc6y-atrc-launches-‘aspire’-drive-creation-future) · [ChallengeON](https://challengeon.atrc.ae/)

**UAE drone seeding**
- [Abu Dhabi Media Office: EAD, ADQ, Dendra](https://www.mediaoffice.abudhabi/en/environment/environment-agency-abu-dhabi-and-adq-partner-with-dendra-to-enhance-terrestrial-and-coastal-restoration-through-advanced-technologies/) · [AGBI](https://www.agbi.com/sustainability/2023/12/abu-dhabi-uses-drones-and-ai-to-reseed-desert-land/) · [Zawya: 6.5M seeds](https://www.zawya.com/en/special-coverage/zawya-green/environment-agency-abu-dhabi-disperses-65mln-native-seeds-using-drones-slc62u2s) · [Gulf News: 10M seeds](https://gulfnews.com/uae/environment/how-abu-dhabi-plans-to-revive-its-deserts-with-10-million-seeds-1.500628192) · [EAD: mangroves](https://www.ead.gov.ae/en/Media-Centre/News/0-plants-one-million-mangrove) · [Middle East AI News: drones in the Gulf](https://www.middleeastainews.com/p/can-drones-reforest-the-gulf-region)

**Seed balls and SETs**
- [Johnstone et al. 2026](https://onlinelibrary.wiley.com/doi/10.1111/rec.70303) · [Organic seed balls 2026](https://link.springer.com/article/10.1007/s11104-026-08530-7) · [Brazil landfill 2026](https://link.springer.com/article/10.1007/s11355-026-00736-2) · [NZ 2025](https://www.tandfonline.com/doi/full/10.1080/0028825X.2024.2432314) · [Seedball review](https://www.researchgate.net/publication/384848426_Seedball_Technology_Facets_and_Prospects_for_Restoration_of_Degraded_Lands) · [Pelletizing review](https://www.researchgate.net/publication/336152944_Review_of_seed_pelletizing_strategies_for_arid_land_restoration) · [Habitat Authority 2011](https://www.habitatauthority.org/fc/studies/Seed-Ball-Experiment-Report-January-2011.pdf) · [Madsen: SETs](https://www.researchgate.net/publication/313991670_Emerging_seed_enhancement_technologies_for_overcoming_barriers_to_restoration) · [Global SET review](https://www.sciencedirect.com/science/article/abs/pii/S0048969721041681) · [Extruded pellets 2024](https://onlinelibrary.wiley.com/doi/full/10.1111/emr.12600) · [Extruded pellets 2023](https://onlinelibrary.wiley.com/doi/10.1111/rec.13857) · [Seed priming + extrusion](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0204380) · [Activated carbon pellets 2026](https://onlinelibrary.wiley.com/doi/10.1111/rec.70316) · [Seedballs Kenya](https://www.globallandscapesforum.org/wp-content/uploads/2018/09/Seedballs-Kenya-Overview-GLF-2018-compressed.pdf) · [Aerial seeding (Wikipedia)](https://en.wikipedia.org/wiki/Aerial_seeding) · [Self-burying carriers, Nature](https://www.nature.com/articles/s41586-022-05656-3) · [UAV seeding review](https://www.tandfonline.com/doi/full/10.1080/00049158.2024.2343516)

**Species**
- [Cyperus conglomeratus, UAEU](https://scholarworks.uaeu.ac.ae/all_theses/651/) · [Stipagrostis, camel rangeland](https://www.researchgate.net/publication/368673377_Improving_seed_germination_of_native_species_for_camel_rangeland_restoration_effects_of_cold_stratification_and_temperature) · [Stipagrostis hydrothermal](https://www.sciencedirect.com/science/article/abs/pii/S0048969725009830) · [Eremobium dormancy chemicals](https://link.springer.com/article/10.1007/s00344-016-9640-z) · [Panicum turgidum maternal effects](https://link.springer.com/article/10.1007/s11756-025-02023-1) · [Panicum salinity, UAE](https://www.ingentaconnect.com/content/ista/sst/2004/00000032/00000003/art00024) · [Gul et al., germination strategies](https://www.halophyte.org/pdfs/drkhan_pdfs/182.pdf) · [Halophytes of Arabian deserts](https://link.springer.com/rwe/10.1007/978-3-030-17854-3_45-1) · [Calligonum fruit colour](https://zuscholars.zu.ac.ae/works/1279) · [Calligonum burial](https://agris.fao.org/search/en/records/65de28d67c7033e84be9f184) · [Calligonum salinity](https://doaj.org/article/9122314ea7354d2b843e0b4f452ceeae) · [UAE vascular flora](https://link.springer.com/chapter/10.1007/978-3-031-37397-8_13)

**Environment, materials, predation**
- [Soils of Abu Dhabi](https://www.researchgate.net/publication/259174728_Soils_of_Abu_Dhabi_Emirate) · [UAE desertification](https://www.researchgate.net/publication/259178629_Soil_and_water_management_for_combating_desertification_-_towards_implementation_of_the_United_Nations_Convention_to_Combat_Desertification_from_the_UAE_perspectives) · [Emirates site data](https://openagriculturejournal.com/VOLUME/18/ELOCATOR/e18743315279696/FULLTEXT/) · [Desert bloom 2026](https://www.thenationalnews.com/news/uae/2026/05/01/the-rains-have-fallen-the-deserts-in-bloom-and-camel-grazing-season-can-begin-a-month-early/) · [Burial depth](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2018.01167/full) · [Biopolymer hydrogel coatings](https://www.nature.com/articles/s41598-025-30594-1) · [Chitosan-alginate](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11818308/) · [Seed coating review](https://link.springer.com/article/10.1007/s43621-026-02826-5) · [Biodegradable SAPs](https://www.hec.edu/en/dare/innovation-entrepreneurship/ab-smart-materials-replacing-microplastic-biodegradable-alternatives) · [Cellulose hydrogels](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10970592/) · [Date palm biochar, sandy soil](https://mrforum.com/product/9781644900178-11/) · [Date palm biochar review](https://link.springer.com/article/10.1007/s12517-022-11123-0) · [Arabian AMF](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8933382/) · [Rodent-deterrent coatings, USDA](https://research.fs.usda.gov/treesearch/61381) · [Savanna seed predation](https://www.sciencedirect.com/science/article/pii/S025462991631105X) · [Desert seed removal](https://www.sciencedirect.com/science/article/abs/pii/S014019631200242X)
