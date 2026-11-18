# Nabat TerraPod Challenge: Research & Brainstorm Notes

*Compiled from a research and brainstorming chat, 2–3 November 2026.*

> **Phase 1 deadline: 19 November 2026** (8–10 slide PDF proposal)
> Challenge page: https://challengeon.atrc.ae/en/challenges/ntpc?lang=en

---

## 1. The challenge

### Who's behind it
- **Organizer: ASPIRE**, the arm of Abu Dhabi's Advanced Technology Research Council (ATRC) that speeds up innovation and runs its "grand challenges" and global competitions.
- **Partner: Nabat**, an Abu Dhabi nature-tech company launched in December 2024 by **VentureOne**, ATRC's commercialisation arm.
  - Uses AI and drones to map sites, seed them from the air, and monitor them by satellite and drone.
  - Its platform is called **NabatOS**.
  - Started with the UAE's national mangrove program (millions of mangroves planted) and now covers coastal, marine and dryland ecosystems.
  - One report says it has helped seed more than 500 ha of land with the Environment Agency – Abu Dhabi (EAD).
  - The challenge is not a weekend hackathon. It's an innovation challenge that runs about 8 months from launch to award.

### The task
> *How might we develop a low-cost, drone-deployable seed pod that holds several native UAE seeds of different sizes and significantly improves vegetation establishment in desert and arid environments?*

The pod must improve germination, break seed dormancy and help early survival against extreme heat, wind, water scarcity, poor and salty soil, and seed predation. It must be cheap to produce at scale.

### Hard specs
| Requirement | Value |
|---|---|
| Size | **2.5–3 cm** diameter. Any shape: sphere, egg, cylinder, disk, etc. |
| Drop survival | **12–15 m** drop from Nabat's drone |
| Handling | Must not break down during loading or pre-flight handling |
| Cost | **≤ AED 0.4 per pod (about US$0.11)**, with cost drivers, assumptions, and 5-year production capacity |
| Materials | Biodegradable, non-toxic, **no microplastics** |
| Planting conditions | Must cope with variable temperature, humidity, sun, salinity, soil type and watering |
| Seeds | **One of 2 mixes**, 3 species each. You set the ratio and the number of seeds per species per pod |

### The six species
| Mix | Species | Family | Type | Dormancy | Seed size (cm) | Weight per 1000 seeds |
|---|---|---|---|---|---|---|
| A | *Eremobium aegyptiacum* | Brassicaceae | Annual | None or physiological | 0.05–0.10 | 0.18 g |
| A | *Cyperus conglomeratus* | Cyperaceae | Perennial sedge | Minimal | 0.10–0.20 | 0.42 g |
| A | *Stipagrostis plumosa* | Poaceae | Perennial grass | Shallow physiological | 0.20–0.30 | 0.85 g |
| B | *Panicum turgidum* | Poaceae | Perennial grass | Minimal | 0.20–0.30 | 1.52 g |
| B | *Calligonum comosum* (arta) | Polygonaceae | Perennial shrub | **Physical (hard seed coat)** | 0.20–0.60 | 2.98 g |
| B | *Haloxylon salicornicum* | Amaranthaceae | Perennial shrub | Short physiological | 0.20–0.30 | 1.24 g |

### Timeline
| Phase | When | What |
|---|---|---|
| **1. Proposal** | Sept 2026 – **19 Nov 2026** | Register, fill in the form, upload an **8–10 slide PDF (max 10 MB, English)**. Semi-finalists notified in Nov 2026 |
| **2. Video pitch** | Dec 2026 | Short live video pitch. Finalists notified in Dec 2026 |
| **3. Field validation** | Jan – Feb 2027 | Ready-made pods due **1 Jan 2027**. Nabat drops them in uncontrolled desert sites for 8–10 weeks |
| Review | Mar 2027 | Holistic panel review |
| Winner | Q2 2027 | Announcement |

If a finalist can't make ready-to-deploy pods, they can send their recipe and clear assembly instructions so ASPIRE assembles them. Nabat supplies the seeds in that case.

### What the Phase 1 deck must cover
1. Team overview and relevant experience (ability to deliver)
2. Pod composition (seeds per species per pod), dimensions, preparation method, deployment method, and drone compatibility
3. **Historical deployment evidence and success rate, with references**
4. **Germination data compared with nearby untreated reference sites**
5. Cost per pod (≤ AED 0.4)
6. Sustainability and biodegradability (non-toxic, no microplastics)
7. Production capacity and scalability over 5 years
8. Readiness: prototype status, or a credible plan to build one

### Scoring
- **Phase 1** (weights not published): quality and sustainability · germination effectiveness · cost effectiveness · drone integration · production and scalability
- **Phase 2:** experience and track record (development history, success rate, any desert testing) · team competence
- **Phase 3:** germination **above the nearby reference areas** · works with Nabat's drone

### Prize and IP
- **US$50,000** to the winner, plus field piloting and possible partnership talks.
- **IP:** you keep it. Nabat gets a non-exclusive, perpetual licence. Nabat may ask to discuss an exclusive licence after the competition, and that may be a condition of paying the prize.
- **Eligibility:** anyone, including students, researchers, startups and companies. The page says "Individual participation" and "Participate multiple times," so more than one proposal may be allowed, such as one per mix.
- **Rules tab:** it didn't load without logging in. **Read it after registering.**
- **Questions:** use the platform's chat with the admins.

---

## 2. What already exists

### Commercial drone-seeding pods
- **AirSeed** (Australia), **Flash Forest** (Canada, "100+ proprietary pod recipes," fires one pod per second), **Dendra**, and **Mast Reforestation** (formerly DroneSeed).
- They all keep their recipes secret, and there's **little independent evidence** of how well they work.

### Research
- **A test of AirSeed's pods (Macquarie University thesis):** glasshouse trials found most species emerged poorly, so **one recipe doesn't suit all seeds**. Seeds placed **near the edge of the pod did better**.
- **Extruded seed pellets (Madsen et al. 2016, sagebrush):** pellets made from a seed "dough" raised emergence **2.3–10×**, partly because the pellet swells and opens channels for the seedling. Pellets with pre-soaked seed (Madsen 2018) gave 2.9–3.8× higher grass density. **Caveat:** an arid Pilbara trial found some pellet seedlings came up and then died.
- **Self-burying wood carriers (CMU, *Nature* 2023):** modelled on *Erodium* seeds, these drill into soil when wet and reached 80% establishment versus about 0% for natural seeds on some ground. They're elegant but lab-only, the tails tangle in the drone hopper, and they almost certainly can't hit AED 0.4.
- **Chili/capsaicin coatings** clearly cut rodent seed predation (Lanni 2024; Pearson 2018). The effect **fades as the coating weathers**, and there's no evidence on ants.
- **Arid pelletizing review (*Restoration Ecology*):** pellets are viable as long as they don't suppress germination themselves, but there are **no formal guidelines** yet. That gap is an opportunity.

### Local context
- **EAD is dropping 10 million native seeds** by air across Al Shuwayb, Sweihan, Nahil, Al Hayer, Al Rawdah, Al Ghada and the Houbara Protected Area.
  - Species include Ghaf, Samar, **Arta**, Shoua, Raghal and Thamam.
  - Some seeds go in moisture-retaining pellets made from natural materials.
- **Species notes:**
  - *Calligonum* germination drops with deeper sand burial and with salinity above about 100 mM, and fruit colour affects germination.
  - *Haloxylon* tolerates up to about 400 mM NaCl and recovers well after salt stress.

---

## 3. Brainstorm: general design directions

**Key insight:** the field test runs in Jan–Feb, which is the UAE's rainy season, but rain there is sparse and unpredictable. Whichever pod lets seeds **germinate and survive on one small rain event** wins.

1. **Layered pod.**
   - Outer shell of clay, chili and a binder: handles the drop, wind and predators.
   - Middle layer of biodegradable hydrogel and biochar: stores water.
   - Seeds sit near the outer edge.
   - Hydrogel options: alginate, chitosan, CMC or starch-based. **Avoid polyacrylamide or polyacrylate hydrogels**, which break the no-microplastics rule.
2. **Pre-treat each species before encapsulating.** Scarify *Calligonum* (hot water, acid or mechanical abrasion), pre-soak (prime) the grasses, and keep tiny *Eremobium* seeds at the surface. A one-size recipe is the known failure mode.
3. **Shape against wind.** A shape that lands flat or seed-side down and doesn't roll.
4. **Release only when it rains.** The pod stays sealed until it gets properly wet, so seeds don't start germinating on dew and then die.
5. **Local, circular materials.** Date-palm fibre, ash or biochar from UAE palm waste, local clay, and composted camel or goat manure. These cut cost and give a strong sustainability story.
6. **Microbes.** Salt-tolerant growth-promoting bacteria or mycorrhizal fungi taken from around the roots of native species, or cyanobacteria that form protective soil crusts.
7. **Choose the mix strategically.**
   - **Mix B** has larger seeds and fills a pod more easily, but *Calligonum*'s hard coat must be dealt with.
   - **Mix A** has tiny seeds, so you can pack many per pod, but they are fragile.
   - If multiple entries are allowed, submit one for each.

**Rough numbers:** a 3 cm sphere is about 14 cm³, so roughly 17–21 g of clay-compost. AED 0.4 is about 11 US cents for materials, manufacturing and seeds combined, which points to **extrusion or press-moulding**, not hand-rolling.

---

## 4. Shape exploration

### 4a. Would a disk help, given that edge seeds did better?

**Why edge seeds probably did better** (the mechanism wasn't established):
1. Less material to push through.
2. Better access to light, oxygen and soil.
3. Seeds in the centre may sit in conditions that are too wet, too dense or low in oxygen.

**Geometry** (3 cm across):
| Shape | Volume | Share within 3 mm of surface |
|---|---|---|
| Sphere, 3 cm | 14.1 cm³ | ~49% |
| Disk, 3 cm × 1 cm | 7.1 cm³ | ~74% |
| Disk, 3 cm × 6 mm | 4.2 cm³ | ~100% |

**Trade-offs:**
- **Water:** a high ratio of surface to volume means **faster drying** and less water per seed, which is bad in the desert.
- **Landing:** a disk lands flat. The bottom face gets soil and shade, while the top face gets roasted. That suggests an asymmetric, bottom-weighted design.
- **Wind:** a disk lying flat doesn't roll like a sphere. Good.
- **Drop** (rough physics estimates, not measured):
  - A ~20 g sphere dropped from 15 m hits at about 15–17 m/s.
  - A ~10 g disk falling flat tops out around 14 m/s, but wobbles, often lands **edge-first** (chipping), and **drifts** in wind.
- **Drone handling:** disks can stack or jam in a dispenser.

**Middle options:** a lens or thick puck (domed top, flat heavy bottom, seeds in a bottom ring), or a sphere with a **core-shell** layout (water-storage core, thin seed-carrying outer layer).

### 4b. A donut (ring) pod

**Geometry:** a ring 3 cm across with a ~1 cm tube and ~1 cm hole has **about 5 cm³ of volume, with about 84% of the material within 3 mm of a surface.**

**What the hole adds:**
1. **A small water trap.** Rain and condensation run off the ring into the hole and wet the soil at the centre, like a miniature zaï pit or half-moon catchment.
2. **A sheltered spot for seedlings.** Seeds sit on the **inner wall facing the hole**. Seedlings come up shaded, out of the wind and away from sand-blasting. The ring acts like a tiny "nurse" structure.
3. **It traps a little sand.** Blown sand settles in the hole and lightly buries the seeds.
4. **It works whichever way up it lands.** A ring is the same top and bottom, so the inner rim touches soil either way.
5. **It hides seeds.** Seeds on the inner wall are less visible to birds and rodents. Put the chili coating on the outside.

**Risks:**
- **Drying out:** lots of surface area. Pack the tube with water-holding material and consider a less permeable skin.
- **Landing on its edge:** a ring can roll like a wheel. A flatter, washer-like tube helps.
- **The drop:** a thin tube can snap at the point of impact.
- **Chaining in the hopper:** **keep the hole smaller than the tube thickness**, or rings can hook into each other.
- **Fewer seeds:** less volume per pod. Fine for Mix A, tighter for Mix B.

**Manufacturing:** a pellet press with a central-pin die, like the way Polo mints are made, can produce ring pods at volume and cost.

**"Crater" variant:** a ring with a thin, quick-dissolving floor across the hole. It holds water in the cup after rain, then the floor breaks down so roots reach the soil.

### 4c. A donut with crimped edges (current favourite)

**Two kinds of crimp:**
- **A. In-plane teeth**, like a bottle cap or gear, pointing outward around the rim.
- **B. Out-of-plane waves**, like a pie crust, rippling up and down.

**What crimping could add:**
1. **Anchoring.** The teeth bite into sand and work like cleats. Wavy rims **stop the ring rolling on its edge**, so it topples flat. That fixes the plain ring's main weakness.
2. **Shock absorption.** The crimps act as a sacrificial crumple zone that chips on impact and protects the seed-carrying core during the 15 m drop.
3. **Water channels.** Ridges give dew more surfaces to condense on. Valleys that **slope toward the hole** guide water into the centre.
4. **Sand catching.** The valleys trap blown sand, anchoring the pod and lightly burying the seeds.
5. **More sheltered spots.** Tiny Mix A seeds go in the outer valleys and the larger seeds on the inner wall. Each species gets its own spot in one pod.

**Risks and fixes:**
| Risk | Why | Fix |
|---|---|---|
| Dust and crumbling while handling | Sharp crimps wear off in the hopper | Shallow (1–2 mm), **rounded** crimps and a firmer skin |
| Jamming in the dispenser | Gear-style teeth can mesh | Prefer waves (B), or uneven tooth spacing |
| Faster drying | More surface area | Low-permeability skin, water reserve in the core |
| Out of spec | Teeth add width | **≤ 3 cm measured tip to tip** |
| Odd flight | Rough edges may wobble differently | Test it |

**Cost:** crimping is essentially free. It's just the shape of the press die, with no extra step or material.

**Recommendation:** shallow, rounded, **wavy (B)** crimps whose valleys slope toward the hole.

**Pitch story:** *the ring catches water, the inner wall shelters the seedlings, and the crimped edge anchors the pod and absorbs the drop.*

---

## 5. Test plan (to produce real Phase 1 data)

Make each shape from the **same recipe**:

| Test | Sphere | Plain ring | Crater ring | Crimped ring (waves) | Crimped ring (teeth) |
|---|---|---|---|---|---|
| Emergence in sand trays vs bare seed, limited watering | | | | | |
| Drying rate: weigh daily after one wetting | | | | | |
| 15 m drop: core intact? lands flat? | | | | | |
| Fan test: slides or rolls? | | | | | |
| Shake test: material lost after 5 min tumbling in a jar (simulates the hopper) | | | | | |

---

## 6. Gaps for a student team, and fixes

- **The deck asks for historical deployment and germination data, and Phase 2 scores track record.**
  - Start germination trials **now**. Most of these grasses germinate within days.
  - **Film a real 15 m drop test**, for example from a building or stairwell. It gives you data and Phase 2 footage.
  - Cite the literature in section 2 as your evidence base.
  - Bring in a faculty supervisor or lab partner for credibility.
- **Getting the seeds:** try local native-seed suppliers or university herbaria, or test with close substitute species and say so openly.
- **Scoring weights aren't published**, so cover all five Phase 1 criteria evenly.

## 7. Open questions for the challenge admins
- Does a ring, disk or crimped shape count as within "2.5–3 cm diameter"? Is it measured across the widest point, with no thickness limit?
- Are team entries allowed, or individual only? Can we submit more than one proposal (one per seed mix)?
- How does Nabat's drone load and release pods (hopper shape, release mechanism)?
- What's in the Rules tab?

---

## Sources
- [Challenge home](https://challengeon.atrc.ae/en/challenges/ntpc?lang=en) · [Challenge statement](https://challengeon.atrc.ae/en/challenges/ntpc/pages/challenge-statement?lang=en) · [Phases & evaluation](https://challengeon.atrc.ae/en/challenges/ntpc/pages/timeline?lang=en) · [FAQ](https://challengeon.atrc.ae/en/challenges/ntpc/pages/faq?lang=en)
- [Nabat launch (Bernama)](https://bernama.com/en/press/news.php?id=2373186) · [Middle East AI News](https://www.middleeastainews.com/p/atrc-ai-robotics-venture-nabat) · [Aletihad on Nabat](https://en.aletihad.ae/news/uae/4544901/nabat-s-ai-powered-ecosystem-restoration-efforts-showcased-a) · [EAD/Nabat drone mangrove planting in Bahrain](https://www.mediaoffice.abudhabi/en/environment/in-cooperation-with-nabat-environment-agency-abu-dhabi-showcases-innovative-use-of-drones-to-plant-mangroves-in-bahrain-as-part-of-abu-dhabi-mangrove-initiative/)
- [Gulf News: Abu Dhabi's 10 million seeds](https://gulfnews.com/uae/environment/how-abu-dhabi-plans-to-revive-its-deserts-with-10-million-seeds-1.500628192)
- [Macquarie seed-coating / drone revegetation thesis](https://figshare.mq.edu.au/articles/thesis/Assessing_the_efficacy_of_artificial_seed-coatings_and_microbial_amendments_for_drone-facilitated_revegetation/21561906) · [Review of seed pelletizing for arid land restoration](https://experts.arizona.edu/en/publications/review-of-seed-pelletizing-strategies-for-arid-land-restoration/) · [Madsen et al. 2016 extruded pellets](https://osuseafoodlab.oregonstate.edu/sites/agscid7/files/eoarc/attachments/903_extruded_seed_2016.pdf)
- [CMU self-burying seed carrier](https://www.cmu.edu/news/stories/archives/2023/february/biodegradable-seed-carrier.html) · [The Conversation: drone seeding critique](https://theconversation.com/drone-seeding-and-e-seeds-sound-exciting-but-ecosystem-restoration-needs-practical-solutions-204274)
- [Capsaicin coatings (Lanni et al. 2024)](https://orrocklab.zoology.wisc.edu/wp-content/uploads/sites/1134/2024/03/Lanni-et-al-CJFR-2024.pdf) · [Pepper coatings explainer](https://thesciencebreaker.org/breaks/plant-biology/spicing-up-restoration-can-a-dash-of-pepper-powder-defend-native-plants)
- [Calligonum salinity (JKSUS)](https://doaj.org/article/9122314ea7354d2b843e0b4f452ceeae) · [Calligonum sand burial](https://agris.fao.org/search/en/records/65de28d67c7033e84be9f184) · [Calligonum fruit colour (Zayed University)](https://zuscholars.zu.ac.ae/works/1279) · [Haloxylon germination](https://pred.uni-regensburg.de/id/eprint/168/)
- [Flash Forest](https://refractor.io/environment/flash-forest-drones-reforestation/)
