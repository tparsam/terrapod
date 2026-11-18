# TerraPod Phase 1 deck: build guide

Everything you need to build the Phase 1 deck with Claude, in the look of
[elevenplantsfordumdums.com](https://www.elevenplantsfordumdums.com/). No design plugins needed.

**Deadline: 19 Nov 2026.** Submit a **PDF, 8 to 10 slides, max 10 MB, in English**, plus the online
participation form. This guide makes a 10-slide 16:9 PowerPoint (`.pptx`) that you export to PDF.

Contents: [1. Setup](#1-setup-15-minutes) · [2. The look](#2-the-look-design-system) ·
[3. Slide by slide](#3-slide-by-slide-content) · [4. Things only you can fill in](#4-things-only-you-can-fill-in) ·
[5. The prompt for Claude](#5-the-prompt-to-paste-into-claude) · [6. Check and submit](#6-check-before-you-submit)

---

## 1. Setup (15 minutes)

### 1.1 Get the files

Accept the GitHub invite (email or github.com), then either:
- **Easy:** on https://github.com/tparsam/terrapod click **Code → Download ZIP** and unzip it, or
- **Terminal:** `git clone https://github.com/tparsam/terrapod.git`

You need these files from it:

| File | What it is |
|---|---|
| `deck/DECK-GUIDE.md` | This guide (Claude reads it too) |
| `final-design.md` | The full design: every number on the slides comes from here |
| `deck/assets/pod_mixA_ring_angle.png` | Mix A pod render, 3/4 view, transparent background |
| `deck/assets/pod_mixA_ring_top.png` | Mix A pod, top view |
| `deck/assets/pod_mixB_disc_angle.png` | Mix B pod render, 3/4 view |
| `deck/assets/pod_mixB_disc_top.png` | Mix B pod, top view |

### 1.2 Install the four fonts (all free, Google Fonts, SIL Open Font License)

Download each one, unzip, and double-click the `.ttf` files to install (Mac: Font Book → Install; Windows:
right-click → Install for all users). **Install the static `.ttf` files** from the `static` folder where
there is one, not only the "variable" file: PowerPoint handles static fonts more reliably.

| Font | Role | Link |
|---|---|---|
| **Unbounded** (Bold, Black) | Big caps headlines with the hard shadow (stands in for the site's custom "Dum dum" face) | https://fonts.google.com/specimen/Unbounded |
| **Ultra** | Huge display titles (used on the site itself) | https://fonts.google.com/specimen/Ultra |
| **Inknut Antiqua** (Regular, Bold) | Huge serif display titles (used on the site itself) | https://fonts.google.com/specimen/Inknut+Antiqua |
| **Hanken Grotesk** (Regular, Medium, Bold, Bold Italic) | Body text, labels, Latin names in italic (stands in for the site's Styrene A, which is paid) | https://fonts.google.com/specimen/Hanken+Grotesk |

Restart PowerPoint or Keynote after installing.

### 1.3 Set up Claude (pick one)

**Option A: claude.ai in the browser (simplest).**
1. A **Pro** (or higher) plan.
2. Settings → **Capabilities** (called "Feature preview" in some versions) → turn on **"Code execution and file
   creation"**. This lets Claude write a real `.pptx` file you can download.
3. Start a new chat, attach the files from 1.1, and paste the prompt from section 5.

**Option B: Claude Code (the terminal app).**
1. Install: https://claude.com/claude-code (`npm install -g @anthropic-ai/claude-code`, then run `claude`).
2. Install Python 3 and the library Claude will use: `pip install python-pptx pillow`.
3. In the unzipped repo folder, run `claude` and paste the prompt from section 5.
   Claude reads the files directly, so you don't attach anything.

**Either way,** Claude builds the deck with the `python-pptx` library. Its own preview won't show our fonts
(they aren't installed where Claude runs), so the preview looks plainer. **Judge it only after you open the
`.pptx` on your computer** with the fonts installed.

### 1.4 You also need

- **PowerPoint or Keynote** to open the `.pptx`, fix small things and export the PDF. Google Slides works
  too, but it only uses Google Fonts loaded in Slides (all four above are available there).
- About **2 hours**: 30 minutes for Claude's first version, the rest for fixes, the team text and checking.

---

## 2. The look (design system)

Taken from the site's own CSS and screenshots, adapted for slides.

### 2.1 What makes the site look like itself

1. **Three greens and a cream, nothing else.** Bright leaf green, deep forest green, cream.
2. **Huge type that plants overlap.** Giant display words with plant images sitting on top of and behind them.
3. **A different display typeface per section.** Every plant gets its own font. We use two (Ultra and
   Inknut Antiqua) and alternate them, so the deck stays readable.
4. **Big caps headline with a hard, offset shadow** (no blur): cream letters, forest-green shadow below-right.
5. **A small outlined number tag**, `#1`, `#6`, centred at the top of each section.
6. **Small bold label above the big title** (the plant's common name), and the **Latin name in bold italic**.
7. **Vertical side labels**: little facts rotated 90° along the left and right edges ("Propagate with cuttings").
8. **Cream oval frames** holding the images on the green background.
9. **Duotone images**: photos turned into shades of green on cream.
10. **A tiny italic credit line** at the bottom of each section (on the site it names the font; we use it for sources).
11. **Playful, short copy** ("Love, water & treat 'em right… serenade often."), but our deck is a proposal,
    so keep the jokes to the cover tagline and the odd side label.

### 2.2 Colours (exact hex values from the site's CSS)

| Name | Hex | Use |
|---|---|---|
| **Leaf** | `#62B16F` | Background of cover and "big moment" slides |
| **Cream** | `#FAF3D3` | Background of content slides; text and ovals on Leaf and Forest |
| **Forest** | `#273326` | All text on Cream; dark slide background |
| **Moss** | `#44714A` | Hard shadow behind caps headlines; outlines; chart bars |
| **Pine** | `#325637` | Second dark (gradient end, table header) |
| **Fern** | `#4A8B55` | Second chart colour, thin rules |
| **Mint** | `#B9E1BF` | Highlights and big numbers on Forest slides |

Rules: text on Cream is always Forest. Text on Leaf is Cream (headlines) or Forest (body). Text on Forest
is Cream or Mint. **No other colours. No gradients except Forest → Pine on dark slides. No soft drop shadows,
no glow, no rounded-corner cards with shadows.**

### 2.3 Fonts and sizes (16:9, 13.333 × 7.5 in)

| Element | Font | Size | Style |
|---|---|---|---|
| Caps headline (cover, Leaf slides) | Unbounded Black | 54–72 pt | ALL CAPS, Cream, hard shadow (2.5) |
| Display title (content slides) | Ultra **or** Inknut Antiqua (alternate slide to slide) | 54–96 pt | Sentence case, Forest or Leaf, tight line spacing (0.9) |
| Label above the title | Hanken Grotesk Bold | 16 pt | Forest |
| Body | Hanken Grotesk Regular | 15–18 pt | Line spacing 1.3 |
| Latin names | Hanken Grotesk Bold Italic | same as body | |
| Table text | Hanken Grotesk Regular / Bold header | 12–14 pt | |
| Number tag | Hanken Grotesk Bold | 14 pt | `#01` … `#10` |
| Side labels | Hanken Grotesk Medium | 11 pt | Rotated 270° (left) / 90° (right) |
| Credit / source line | Hanken Grotesk Italic | 9–10 pt | Bottom centre |

At most **two display words styles per slide** (one display title + body). Never more than ~40 words of body
text per slide outside tables.

### 2.4 The building blocks

- **Hard-shadow headline.** Two identical text boxes: the back one in Moss `#44714A`, moved **0.05 in right
  and 0.05 in down**; the front one in Cream on top. (Don't use PowerPoint's shadow effect: it blurs and
  doesn't survive PDF export or Google Slides consistently.)
- **Number tag.** A small square text box, about 0.55 × 0.45 in, **2 pt Forest outline** (Cream outline on
  dark slides), no fill, text `#01` centred, placed **top centre**, 0.4 in from the top.
- **Oval frame.** An ellipse, Cream fill, no outline, about 2.9 × 3.8 in (taller than wide), with a
  transparent pod render placed on top, centred, about 75% of the oval's width. Small caption under it in
  Hanken Grotesk 10 pt Cream.
- **Side labels.** Text boxes rotated 270° on the left edge and 90° on the right edge, vertically centred,
  0.35 in from the edge.
- **Credit line.** One line, bottom centre, 0.3 in from the bottom: sources in italic.
- **Tables.** No vertical lines, no fills except a Pine header row with Cream text on Leaf/Forest slides, or a
  Forest header on Cream slides. Thin Fern rules between rows.
- **Charts.** Native PowerPoint bar charts (so they stay editable), bars in Moss and Mint, no gridlines, no
  3D, data labels on the bars, Hanken Grotesk.
- **Margins.** 0.6 in all round. Keep the centre column for the main title, like the site.

### 2.5 Slide layouts (each slide uses one)

| Layout | Background | Structure |
|---|---|---|
| **L1 Cover** | Leaf | Small corner texts top-left and top-right, caps headline centre (hard shadow), centred numbered list, an oval at each side, tagline at bottom |
| **L2 Editorial** | Cream | Number tag, label, huge display title (centre), body below in 2 or 3 columns, side labels, credit line |
| **L3 Showcase** | Leaf | Number tag (Cream outline), caps headline, two ovals side by side with specs under each |
| **L4 Big numbers** | Forest → Pine gradient | Number tag (Cream), display title in Leaf `#62B16F` (like the site's "Staghorn Fern"), 3 or 4 huge Mint numbers with short Cream captions, optional chart |
| **L5 Table** | Cream | Number tag, label, display title (smaller, 48–54 pt), one clean table, credit line |

Rhythm: L1 → L2 → L3 → L2 → L4 → L5 → L4 → L5 → L2 → L3. Backgrounds alternate, the way the site's
sections do.

---

## 3. Slide by slide (content)

All copy below is final unless marked **[FILL]**. Numbers come from `final-design.md`; don't change them
without checking there. **No em dashes in the slide text** (they read as machine-written); use commas,
colons or full stops.

### Slide 1: Cover (L1, Leaf)

- Top-left (Hanken 11 pt, Forest): `Nabat TerraPod Challenge` / `Phase 1 proposal, Nov 2026`
- Top-right (Hanken 11 pt, Forest, right-aligned): `100% biodegradable` / `0% microplastics`
- Caps headline (Unbounded Black ~64 pt, Cream, hard shadow, 2 lines):
  `TWO PODS FOR A`
  `GREENER DESERT`
- Centred list under it (Hanken Bold 15 pt Forest, Latin names Bold Italic), exactly like the site's plant list:
  - `Mix A,  Eremobium aegyptiacum · Cyperus conglomeratus · Stipagrostis plumosa`
  - `Mix B,  Panicum turgidum · Haloxylon salicornicum · Calligonum comosum`
  - then a blank line and `Team: [FILL: Name 1] & [FILL: Name 2]`
- Left oval: `pod_mixA_ring_angle.png`, caption `Mix A pod, 26 mm`
- Right oval: `pod_mixB_disc_angle.png`, caption `Mix B pod, 26 mm`
- Bottom tagline (Unbounded Bold 20 pt Cream, letter-spaced, small hard shadow):
  `DROP 'EM FROM 15 M… WATCH 'EM GROW.`

### Slide 2: Why seed balls fail, and what we changed (L2, Cream, Inknut Antiqua)

- Tag `#02` · Label: `The problem`
- Display title: `Most seed balls bury the seed.`
- Three columns (bold first line, then 1–2 lines):
  1. **Seeds in the wrong place.** In pellets, small seeds near the edge came up **28× better** than seeds in
     the centre; with seeds in the centre, bare seed beat the pellets. **TerraPod: seeds sit in a thin skin on
     both faces, so a seeded face always lands on the soil.**
  2. **Pods that roll or stand on edge.** A pod resting on its rim has no seed touching the ground. **TerraPod:
     rounded lobes and a rounded rim; in 200 simulated landings it ended on its edge 0.5% of the time
     (25% without the rounded rim).**
  3. **Eaten before they sprout.** Harvester ants and rodents take exposed seed. **TerraPod: a fine-sand outer
     dust: a sand coat cut ant predation in 48 of 53 species.**
- Left side label: `28× better emergence near the surface`
- Right side label: `How TerraPod improves on existing carriers`
- Credit line: `Sources: Lieurance et al. 2024; Brown et al. 2023; LoPresti et al. 2019, Ecology (see final-design.md §2, prior-art.md §9.7)`

### Slide 3: Two pods, one production line (L3, Leaf)

- Tag `#03` · Caps headline (Unbounded, hard shadow, 48 pt): `ONE PRESS. TWO PODS.`
- Left oval: `pod_mixA_ring_angle.png`. Under it (Cream title, Forest body):
  - **Mix A: thin lobed ring**
  - `26 mm across · 6.4 mm thick · about 2.7 g`
  - `Small surface seeds need no thick core. The hole catches water and blown sand, and pods stack on a rod.`
- Right oval: `pod_mixB_disc_angle.png`. Under it:
  - **Mix B: lobed disc**
  - `26 mm across · 9.4 mm thick · about 4.2 g`
  - `Thick enough to bury the big Calligonum seed in the core. No hole, so about 10× harder to crack.`
- Bottom line (Hanken Bold 14 pt Forest, centred):
  `Same recipe, same press, same seed skin: only the mould changes. Drop both pods together for all six species at every site.`
- Credit line: `Sizes after drying; mass at an assumed 1.2 g/cm³. Inside the 2.5 to 3 cm rule with margin.`

### Slide 4: What's inside (L2, Cream, Ultra)

- Tag `#04` · Label: `Composition` · Display title: `Seeds where they grow best.`
- **Left half: a cross-section diagram** drawn with PowerPoint shapes (a wide rounded rectangle cut in layers,
  labels on the right with thin Fern leader lines). Top to bottom:
  - `Sand dust, under 0.3 mm: keeps ants off` (thin band, light Cream with Fern outline)
  - `Seed skin, 1.5 mm: low clay + compost + surface seeds` (Mint band with small Forest dots for seeds)
  - `Core: high clay, seed-free, drop strength` (Moss band; in it one small Forest oval labelled `Calligonum (Mix B)`)
  - `Seed skin, 1.5 mm` (Mint, dots)
  - `Sand dust` (thin band)
  - Note under it: `Either face can land down.`
- **Right half: table**, header `Species | Seeds per pod | Where`:

| Species | Seeds per pod | Where |
|---|---|---|
| **Mix A** | | |
| *Eremobium aegyptiacum* | 20 (clusters of about 5) | At the surface |
| *Cyperus conglomeratus* | 10 | At the surface |
| *Stipagrostis plumosa* (bristles removed) | 6 | Bottom of the skin, 1–1.5 mm |
| **Mix B** | | |
| *Panicum turgidum* | 6, flat side out | At the surface |
| *Haloxylon salicornicum* | 6 | Bottom of the skin, 1–1.5 mm |
| *Calligonum comosum* (scarified) | 2 | Centre of the core |

- Small text under the table: `Seeds are split evenly between the two faces. Seed mass: about 13 mg (A), 23 mg (B), under 1% of the pod. At typical 5–25% establishment that is about 2–9 seedlings per Mix A pod and 1–3.5 per Mix B pod; tray trials tune the counts.`
- Credit line: `All seeds soaked in 0.1 mM salicylic acid for better field survival (Pedrini et al. 2021). Full rationale: final-design.md §2.`

### Slide 5: Designed by simulation (L4, Forest)

- Tag `#05` · Display title (Ultra, Leaf green, 60 pt): `Dropped half a million times before we pressed one.`
  > The maths: 4 genetic searches (2 mixes × 2 diameter readings) × about 2,400 designs each × 60 simulated
  > landings = about 576,000 landings. If you'd rather keep it plain, use `Shaped by simulation.`
- Three big Mint numbers (Unbounded Black 60 pt) with Cream captions (Hanken 14 pt):
  - `0.5%` · `of landings end on the pod's edge (25% before we rounded the rim)`
  - `10×` · `harder to crack: Mix B disc vs the same shape with a hole`
  - `11 cm` · `median roll after landing for Mix A (pie-crust crimps rolled about 2× farther)`
- Small chart (optional, right side): native bar chart "Ends on its edge, % of 200 landings": `Lobed ring, square rim: 25` / `Lobed ring, rounded rim: 0.5`.
- Body line (Cream, 13 pt): `A genetic algorithm searched lobe count, depth, hole, thickness and rim. Each design was dropped 60 times in a 3D physics simulation (MuJoCo) and stress-tested with finite-element analysis.`
- Credit line (Cream italic): `Simulations rank shapes on hard ground; bench drop tests from 15 m on sand and firm ground confirm them. Code: github.com/tparsam/terrapod`

### Slide 6: Materials (L5, Cream, Inknut Antiqua)

- Tag `#06` · Label: `Sustainability` · Display title: `Clay, sand, starch. That's it.`
- Table, header `Layer | Recipe | Why`:

| Layer | Recipe (dry weight) | Why |
|---|---|---|
| Sand dust | Fine sand | Mould release; keeps ants off |
| Seed skin | 20% clay, 60% sand, 15% compost, 5% starch | Low clay lets shoots break through; compost feeds them |
| Core | 45% clay, 47% sand, 5% starch, 1.5% date-palm fibre, ≤1% date-palm biochar | Strength for the drop; local date-palm waste |
| Film | Starch:CMC 80:20, thin spray | Holds about 17.5× its weight in water and biodegrades in soil |

- Three small "chips" below (outlined Forest pill shapes, Hanken Bold 13 pt): `Biodegradable` · `Non-toxic` · `No microplastics`
- Line: `We avoid polyacrylamide water crystals (microplastics) and synthetic glue binders. The pod is strong until it lands, then softens with the first rain: in field trials, whether the pellet broke up after landing made no difference to establishment.`
- Credit line: `Teichroew & Rew 2025, Restoration Ecology; starch–CMC hydrogel, Sci Rep 2025. See final-design.md §4.`

### Slide 7: The evidence (L4, Forest)

- Tag `#07` · Display title (Ultra, Leaf green): `Built on what already works.`
- Four stat blocks in a row (Mint number, Cream caption, tiny italic source):
  - `28×` · `better emergence with small seeds near the pellet surface` · *Lieurance et al. 2024*
  - `2.6×` · `more seedlings from low-clay (10%) pellets than controls in the field (2.6 vs 1.0)` · *Teichroew & Rew 2025*
  - `48 / 53` · `species protected from harvester ants by a sand coat` · *LoPresti et al. 2019*
  - `+23%` · `germination from seed coatings across degraded ecosystems` · *Ren et al. 2026, meta-analysis*
- Line (Cream 14 pt): `Our germination data: tray trials comparing TerraPod with bare seed and standard seed balls start now, against untreated reference trays, before the January field validation.`
- Credit line: `Full reference list: prior-art.md in the repo.`

### Slide 8: Cost (L5, Cream, Ultra)

- Tag `#08` · Label: `Cost per pod` · Display title: `Well under 40 fils.`
- Table, header `Item | Mix A | Mix B | Basis`:

| Item | Mix A | Mix B | Basis |
|---|---|---|---|
| Body materials | AED 0.008 | AED 0.013 | 2.7 g / 4.2 g at AED 3/kg **[FILL: replace with a real UAE quote]** |
| Film coat | **[FILL]** | **[FILL]** | Starch + CMC, a few mg per pod |
| Pressing, labour, energy | **[FILL]** | **[FILL]** | Machine cost ÷ output (from a supplier quote) |
| Seeds | Supplied by Nabat | Supplied by Nabat | **[FILL: confirm with organisers; if included, add it]** |
| **Total** | **[FILL]** | **[FILL]** | **Target ≤ AED 0.40** |

- Line: `Main cost drivers: pressing time and seed. Materials are cheap, local and by the tonne: UAE clay, sand and date-palm waste.`
- Credit line: `Assumptions stated; prices to be replaced with supplier quotes.`

> If you can't get quotes tonight, keep the materials line, write "estimate" next to each filled number, and
> say where it came from. Don't invent numbers.

### Slide 9: Production and scale (L2, Cream, Inknut Antiqua)

- Tag `#09` · Label: `Production` · Display title: `From mould to millions.`
- Left: the 7 steps as a numbered list (Hanken 14 pt):
  1. Dust both mould halves with fine sand
  2. Place the surface seeds
  3. Press 1.5 mm of seed-skin mix; add the deeper seeds
  4. Fill with core mix
  5. Mix B: press two scarified *Calligonum* seeds into the centre
  6. Close, press 30 s, trim, dry in shade 48–72 h
  7. Spray the starch–CMC film
- Right: `Scale-up` block:
  - `Now: 3D-printed press moulds (files ready)`
  - `Pilot: manual or pneumatic press with multi-cavity moulds`
  - `Scale: rotary tablet press with layered filling, a standard pharma and food machine`
  - `Capacity: [FILL] pods per hour per press × [FILL] presses = [FILL] million pods per year by year 5`
- Side label (right): `These steps double as ASPIRE's assembly instructions`
- Credit line: `final-design.md §5; research.md §10.`

### Slide 10: Readiness and next steps (L3 variant, Leaf)

- Tag `#10` · Caps headline (hard shadow): `READY TO PRESS.`
- Left column, `Done` (Cream title, Forest body):
  - `Full design and seed placement, backed by published studies`
  - `Shape chosen by genetic search + 3D drop simulation`
  - `Print-ready moulds for both pods`
  - `Bench and tray test protocols`
- Right column, `Next, to 1 Jan 2027`:
  - `Nov: print moulds, measure shrinkage, crush tests`
  - `Dec: 15 m drop tests on sand and firm ground; germination trays`
  - `Late Dec: final recipe; produce pods for the field trial`
  - `Jan to Feb 2027: field validation with Nabat`
- Bottom band, `Team` (Hanken 13 pt Forest): `[FILL: Name 1, one line on background and role]` · `[FILL: Name 2, one line]`
- Bottom line: `Questions for Nabat: how is diameter measured? Which dispenser? Which ground types?`

---

## 4. Things only you can fill in

| Where | What | If you can't |
|---|---|---|
| Slides 1, 10 | Both team names, and one line each on background and role | Required by the rules (topic 1). Keep it honest and short |
| Slide 8 | A real price per kg for clay (and ideally starch, CMC), from any UAE supplier or listing | Keep AED 3/kg and label it "estimate" |
| Slide 8 | Pressing cost per pod | Write "to be quoted" |
| Slide 8 | Whether seed cost counts toward AED 0.40 | Say "assumed supplied by Nabat, to confirm" |
| Slide 9 | Press output per hour | Ask Claude for a typical rotary tablet press output **for large (25–30 mm) tablets, with a source**, and label it as typical |
| Slide 5 | Keep the "half a million times" title only if you're happy with the maths in the note | Use `Shaped by simulation.` |

---

## 5. The prompt to paste into Claude

Copy everything in the box. In claude.ai, attach `DECK-GUIDE.md`, `final-design.md` and the four PNGs from
`deck/assets/` first. In Claude Code, run it from the repo folder.

```
Build a 10-slide 16:9 PowerPoint deck (.pptx) for our Nabat TerraPod Challenge Phase 1 proposal.

Follow DECK-GUIDE.md exactly. It is the spec: section 2 is the design system (colours, fonts, sizes,
building blocks, layouts) and section 3 is the content of every slide. final-design.md is the source of
truth for numbers; do not invent or change any number, citation or claim. Keep every [FILL] marker
visible, highlighted in Mint #B9E1BF, so I can find it.

How to build it:
- Use python-pptx. Slide size 13.333 x 7.5 in. Start from a blank presentation; do not use a template.
- Set font names exactly as written: "Unbounded", "Ultra", "Inknut Antiqua", "Hanken Grotesk". They are
  installed on my computer, not yours, so your preview will show fallback fonts: that is expected.
  Set the font on every run of text explicitly (including table cells and chart labels).
- Colours only from section 2.2.
- Hard-shadow headlines: two stacked text boxes, Moss #44714A behind, offset 0.05 in right and down,
  Cream #FAF3D3 in front. No PowerPoint shadow effects anywhere.
- Number tag "#01".."#10" top centre on every slide, as in section 2.4.
- Ovals: Cream ellipse with the transparent pod PNG centred on top (pod_mixA_ring_angle.png,
  pod_mixB_disc_angle.png).
- Side labels: text boxes rotated 270 deg (left) and 90 deg (right).
- Tables: native tables styled per section 2.4 (no default table style colours, no vertical lines).
- Charts: native python-pptx bar charts, Moss/Mint bars, no gridlines, data labels on.
- Slide 4 cross-section: draw it with rectangles and small ovals, not an image.
- No em dashes in slide text. Max ~40 words of body text per slide outside tables.
- Put the speaker notes for each slide in the notes field: 2-3 sentences I can say out loud.

When done:
1. Save as TerraPod_Phase1.pptx and give it to me to download.
2. Render every slide to PNG (LibreOffice if available) and look at each one. Fix overflowing text,
   overlaps, and anything off the slide, then render again.
3. Tell me: any [FILL] still open, any text you had to shorten, and anything from the guide you could
   not do.
```

**Follow-up prompts that help:**
- `Slide N looks crowded: cut the body text by a third and make the display title bigger.`
- `Make the cover headline bigger and the list smaller, closer to elevenplantsfordumdums.com.`
- `Here are our team details: … Put them on slides 1 and 10.`
- `Here is a clay price: … Update slide 8 and the totals.`

---

## 6. Check before you submit

Open the `.pptx` on your computer (fonts installed) and check:

- [ ] Fonts show correctly: chunky caps (Unbounded), heavy slab (Ultra), quirky serif (Inknut Antiqua).
      If one shows as Arial or Calibri, that font isn't installed: reinstall the static `.ttf` and reopen.
- [ ] 10 slides, 16:9, every slide has its `#NN` tag.
- [ ] Only the seven colours; no blurred shadows, no default blue table styles.
- [ ] No text running off a slide or under an image.
- [ ] All eight required topics are covered (table below).
- [ ] Every **[FILL]** is filled or deliberately labelled "estimate" / "to be confirmed".
- [ ] Numbers match `final-design.md` (sizes 26 mm, 6.4 / 9.4 mm, 2.7 / 4.2 g, 0.5%, 10×, seed counts).
- [ ] Export: **File → Export → PDF** (PowerPoint: "Best for printing" off if the file is too big; Keynote:
      Image quality "Better"). **Under 10 MB.** If it's bigger: PowerPoint → select a picture → Picture
      Format → Compress Pictures → 150 ppi, all pictures, then export again.
- [ ] Open the PDF and check fonts are embedded (text looks right, not substituted).
- [ ] File name: `TerraPod_Phase1_Proposal.pdf`.
- [ ] Upload on the challenge platform with the participation form. **The rules say both "by 19 November" and
      "before 19 November 2026", with no time zone: submit by the end of 18 Nov UAE time to be safe**, or
      ask the organisers in the platform chat right away.

**Required topics (from the challenge rules) and where they are:**

| Required topic | Slide |
|---|---|
| 1. Team overview and experience | 1, 10 |
| 2. Composition (seeds per species per carrier), dimensions, preparation, deployment, UAV fit | 3, 4, 5, 9 |
| 3. Past deployment evidence and success rate, with references | 2, 7 |
| 4. Germination data vs. adjacent reference sites | 7 (published data + our trial plan) |
| 5. Cost per carrier ≤ AED 0.40 | 8 |
| 6. Sustainability and biodegradability | 6 |
| 7. Production capacity and scalability over 5 years | 9 |
| 8. Readiness (prototype or plan) | 10 |
| How it improves on existing carriers | 2 |

---

*Regenerate the pod renders after any design change:* `uv run --python 3.11 deck/make_assets.py`
