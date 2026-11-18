# TerraPod

Our entry for the [Nabat TerraPod Challenge](https://challengeon.atrc.ae/en/challenges/ntpc): a cheap,
biodegradable seed carrier that a drone drops from 12 to 15 m to grow native plants in the UAE desert.
Phase 1 deck due 19 Nov 2026.

**Start with [`final-design.md`](final-design.md)**: the challenge rules, the current design and the decision log.

| File | What it is |
|---|---|
| [`final-design.md`](final-design.md) | The design: rules, seed placement, shape per seed mix, materials, manufacturing, tests |
| [`research.md`](research.md) | Background research: species, soils, seed carriers, costs |
| [`prior-art.md`](prior-art.md) | Who has done similar work, with sources |
| [`nabat-terrapod-notes.md`](nabat-terrapod-notes.md), [`notes.md`](notes.md) | Working notes and challenge summary |
| [`geometry/`](geometry/README.md) | Shape search (genetic algorithm, 3D landing simulation, stress model), press moulds, bench-test protocol |

## Running the geometry code

Needs [`uv`](https://docs.astral.sh/uv/). Each script installs its own dependencies.

```bash
uv run --python 3.11 geometry/ga2.py --cover-min 3.0 --out geometry/out/ga2_mixA   # Mix A shape search (~20 min)
uv run --python 3.11 geometry/ga2.py --cover-min 4.5 --out geometry/out/ga2_mixB   # Mix B shape search (~20 min)
uv run --python 3.11 geometry/mix_compare.py                                       # Mix A vs Mix B ring vs Mix B disc
uv run --python 3.11 --with pytest --with pymoo --with matplotlib --with "mujoco<3.3" pytest geometry -q   # tests
```

Python 3.11 because MuJoCo (the physics engine for the landing simulation) has no package for Python 3.13 on macOS.
Most STL files are not in the repo: the scripts regenerate them. The press moulds to print are kept
(`geometry/out/moulds/`, and `pick_1_mould_half.stl` in each `geometry/out/ga2*/` scenario). Print each mould half twice.
