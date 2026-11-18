"""Physics checks for pod_ga.py. Run: uv run --with pytest --with pymoo pytest geometry -q"""
import math

import numpy as np
import pytest

import pod_ga as pg

G = 9.81


def flat_ring(D=30, hole=10, t=10):
    return pg.Pod(D=D, hole=hole, t_edge=t, dome=0, n=0, a=0, p=1)


def test_ring_volume_matches_analytic():
    vol, mass, inertia = pg.mass_props(flat_ring(), density=1000)
    exact = math.pi * (0.015**2 - 0.005**2) * 0.010
    assert abs(vol - exact) / exact < 0.005
    exact_I = 1000 * math.pi * 0.010 * (0.015**4 - 0.005**4) / 2
    assert abs(inertia - exact_I) / exact_I < 0.01


def test_mesh_watertight_and_volume_agrees():
    pod = pg.Pod(D=28, hole=9, t_edge=8, dome=2, n=12, a=2, p=1.5)
    V, F = pg.surface_mesh(pod)
    edges = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1)
    _, counts = np.unique(edges, axis=0, return_counts=True)
    assert np.all(counts == 2), "every edge must be shared by exactly two faces"
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    mesh_vol = np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6
    grid_vol = pg.mass_props(pod, 1000)[0]
    assert mesh_vol > 0, "faces must point outward"
    assert abs(mesh_vol - grid_vol) / grid_vol < 0.01


def test_fem_matches_brazilian_disc_formula():
    # Solid disc squeezed across its diameter: centre tension = 2P/(pi D t).
    disc = pg.Pod(D=30, hole=0, t_edge=10, dome=0, n=0, a=0, p=1)
    nodes, tris, thick = pg.plane_mesh(disc, n_theta=240, n_r=24)
    P = 100.0
    top, bot = np.argmax(nodes[:, 1]), np.argmin(nodes[:, 1])
    f = np.zeros(2 * len(nodes))
    f[2 * top + 1] = -P
    fixed = [2 * bot, 2 * bot + 1, 2 * top]
    sig = pg.solve_plane_stress(nodes, tris, thick, f, fixed)
    centre = np.argmin(np.linalg.norm(nodes, axis=1))
    near = np.any(tris == centre, axis=1)
    sx = sig[near, 0].mean()
    exact = 2 * P / (math.pi * 0.030 * 0.010)
    assert abs(sx - exact) / exact < 0.10


def test_square_needs_exact_threshold_speed_to_tip_over():
    s = 0.02
    R = s / math.sqrt(2)
    pts = np.array([[1, -1], [1, 1], [-1, 1], [-1, -1]]) * s / 2
    k2 = s**2 / 6
    v_star = R * math.sqrt(2 * G * (R - s / 2) / (k2 + R**2))
    assert pg.roll_polygon(pts, k2, 0.95 * v_star, cap=1.0) == 0
    assert pg.roll_polygon(pts, k2, 1.05 * v_star, cap=1.0) >= s - 1e-12


def test_crimps_stop_rolling_and_smooth_ring_does_not():
    cap = 2.0
    assert pg.roll_distance(flat_ring(), v0=1.0, cap=cap) == cap
    crimped = pg.Pod(D=30, hole=10, t_edge=10, dome=0, n=8, a=3, p=1)
    assert pg.roll_distance(crimped, v0=1.0, cap=cap) < 0.25 * cap


def test_tip_barrier_of_flat_ring():
    R, h = 0.015, 0.005
    exact = math.hypot(R, h) - h
    assert abs(pg.tip_barrier(flat_ring()) - exact) / exact < 0.02


def test_smoke_run_writes_outputs(tmp_path):
    pg.main(["--pop", "12", "--gens", "2", "--picks", "3", "--out", str(tmp_path)])
    assert (tmp_path / "pareto.csv").exists()
    assert (tmp_path / "pareto.png").exists()
    assert (tmp_path / "summary.md").exists()
    assert (tmp_path / "picks.png").exists()
    assert len(list(tmp_path.glob("pick_*.stl"))) == 3


def test_mould_half_is_watertight_and_holds_half_a_pod():
    import moulds

    pod = pg.Pod(D=25, hole=6, t_edge=7.7, dome=0.2, n=4, a=3, p=1)
    V, F, (side, height) = moulds.mould_half(pod, step=0.2, pegs=False)
    edges = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1)
    _, counts = np.unique(edges, axis=0, return_counts=True)
    assert np.all(counts == 2)
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    solid = np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6
    cavity = side**2 * height - solid
    half_pod = pg.mass_props(pod, 1000)[0] / 2
    assert abs(cavity - half_pod) / half_pod < 0.03


def test_analysis_turns_raw_measurements_into_deck_numbers(tmp_path):
    import analyse_tests as at

    pods = {"crush_test_disc": pg.Pod(30, 0, 10, 0, 0, 0, 1), "ring": pg.Pod(25, 6, 8, 0, 0, 0, 1)}
    vol_ring = pg.mass_props(pods["ring"], 1000)[0] * 1e6  # cm^3
    rows = [
        # a ring that dried 2% small: true volume shrinks by 0.98^3
        {"design": "ring", "test": "drop", "surface": "firm", "mass_dry_g": f"{1.5 * vol_ring * 0.98**3:.4f}",
         "diameter_mm": "24.5", "result": "intact"},
        {"design": "ring", "test": "drop", "surface": "firm", "mass_dry_g": "", "result": "broken"},
        {"design": "crush_test_disc", "test": "crush", "diameter_mm": "30", "thickness_mm": "10", "peak_kg": "5"},
        {"design": "ring", "test": "tumble", "mass_dry_g": "4.0", "mass_after_g": "3.8"},
    ]
    path = tmp_path / "data.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        import csv as _csv
        w = _csv.DictWriter(fh, fieldnames=at.COLUMNS)
        w.writeheader()
        w.writerows(rows)
    r = at.analyse(path, pods)
    assert abs(r["ring"]["density_g_cm3"] - 1.5) < 0.01
    assert abs(r["crush_test_disc"]["tensile_kpa"] - 2 * 5 * 9.81 / (math.pi * 0.03 * 0.01) / 1000) < 0.01
    assert r["ring"]["drop_firm_survival_pct"] == 50
    assert abs(r["ring"]["tumble_loss_pct"] - 5) < 1e-9


def test_squeeze_stress_of_disc_is_brazilian_value_per_newton():
    exact = 2 / (math.pi * 0.030 * 0.010)
    assert abs(pg.squeeze_stress(pg.DISC) - exact) / exact < 0.15


def test_drop_estimate_from_strength_and_density():
    import analyse_tests as at

    ring = pg.Pod(25, 6, 8, 0, 0, 0, 1)
    g_max, stop_mm = at.drop_estimate(ring, tensile_kpa=200, density=1.2)
    a = 200e3 / (1200 * pg.impact_stress(ring, mesh=pg.FINE))  # the pod's own weight x a reaches the strength
    assert abs(g_max - a / pg.G) < 1e-9
    assert abs(stop_mm - at.IMPACT_SPEED**2 / (2 * a) * 1000) < 1e-9
    assert at.drop_estimate(ring, 400, 1.2)[1] < stop_mm  # stronger mix needs a shorter stop


def test_analysis_reports_how_deep_pods_sink_into_sand(tmp_path):
    import csv as _csv

    import analyse_tests as at

    path = tmp_path / "d.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = _csv.DictWriter(fh, fieldnames=at.COLUMNS)
        w.writeheader()
        w.writerows([{"design": "ring", "test": "drop", "surface": "sand", "result": "intact", "embed_mm": "12"},
                     {"design": "ring", "test": "drop", "surface": "sand", "result": "intact", "embed_mm": "8"}])
    r = at.analyse(path, {"ring": pg.Pod(25, 6, 8, 0, 0, 0, 1)})
    assert r["ring"]["drop_sand_embed_mm"] == 10


def test_analysis_reports_drying_time_and_wind_stability(tmp_path):
    import csv as _csv

    import analyse_tests as at

    path = tmp_path / "d.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = _csv.DictWriter(fh, fieldnames=at.COLUMNS)
        w.writeheader()
        w.writerows([{"design": "ring", "test": "drying", "dry_hours": "30"},
                     {"design": "ring", "test": "drying", "dry_hours": "40"},
                     {"design": "ring", "test": "fan", "result": "stayed"},
                     {"design": "ring", "test": "fan", "result": "rolled"}])
    r = at.analyse(path, {"ring": pg.Pod(25, 6, 8, 0, 0, 0, 1)})
    assert r["ring"]["dry_hours"] == 35
    assert r["ring"]["fan_stayed_pct"] == 50


# ---------- up-and-down (pie-crust) waves: geometry, 3D physics, moulds ----------

P1 = pg.Pod(25.02, 6, 7.69, 0.2, 4, 2.98, 0.96)
P1R = pg.Pod(25.02, 6, 7.69, 0.2, 4, 2.98, 0.96, rim=2.5)  # pick 1 with a 2.5 mm rounded rim


def _closed_volume(V, F):
    edges = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1)
    _, counts = np.unique(edges, axis=0, return_counts=True)
    assert np.all(counts == 2), "mesh must stay watertight"
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    return np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6


def test_waves_ripple_the_rim_without_changing_volume():
    import waves3d as w3

    flat = _closed_volume(*pg.surface_mesh(P1))
    V, F = w3.wavy_mesh(P1, m=8, b=1.5)
    assert abs(_closed_volume(V, F) - flat) / flat < 1e-3  # a vertical shear keeps volume (to triangulation error)
    lift = V[:, 2] - pg.surface_mesh(P1)[0][:, 2]
    assert abs(lift.max() - 0.0015) < 1e-4  # full amplitude at the rim
    assert np.allclose(w3.wavy_mesh(P1, 0, 0.0)[0], pg.surface_mesh(P1)[0])


def test_3d_sim_ring_at_rest_stays_put_and_lobes_stop_an_edge_roll_sooner():
    import waves3d as w3

    smooth = pg.Pod(25.02, 6, 7.69, 0.2, 0, 0, 1)
    rest = w3.throw(*pg.surface_mesh(smooth), pos_tilt=0.0, v=(0, 0, 0), w=(0, 0, 0))
    assert rest["dist_m"] < 0.002 and rest["flat"]
    roll = dict(pos_tilt=np.pi / 2, v=(1.0, 0, 0), w=(0, 1.0 / 0.0125, 0))  # upright, rolling along +x without slip
    d_smooth = w3.throw(*pg.surface_mesh(smooth), **roll)["dist_m"]
    d_lobed = w3.throw(*pg.surface_mesh(P1), **roll)["dist_m"]
    assert d_lobed < d_smooth


def test_wavy_mould_halves_hold_the_whole_pod():
    import moulds

    total = 0.0
    for side in (1, -1):
        V, F, (s, h) = moulds.mould_half(P1, step=0.2, pegs=False, wave=(8, 1.5), side=side)
        total += s**2 * h - _closed_volume(V, F)
    pod = pg.mass_props(P1, 1000)[0]
    assert abs(total - pod) / pod < 0.03


def test_waves3d_smoke_run_writes_report_plot_and_moulds(tmp_path):
    import waves3d as w3

    w3.main(["2", str(tmp_path)])
    for f in ("results.csv", "results.md", "distances.png"):
        assert (tmp_path / f).exists()
    assert len(list(tmp_path.glob("*_mould_half.stl"))) == 2


def test_rounded_rim_thins_the_outer_edge_and_stays_closed():
    import waves3d as w3

    V0, F = pg.surface_mesh(P1)
    V, F2 = pg.surface_mesh(P1R)
    vol0, vol = _closed_volume(V0, F), _closed_volume(V, F2)
    assert 0.85 * vol0 < vol < vol0  # trims a little material off the rim only
    th = np.arctan2(V[:, 1], V[:, 0])
    at_wall = np.isclose(np.hypot(V[:, 0], V[:, 1]), pg.r_out(P1, th))
    assert np.abs(V[at_wall, 2]).max() < 0.4 * np.abs(V0[at_wall, 2]).max()


def test_rounded_rim_mould_holds_half_the_rounded_pod():
    import moulds
    import waves3d as w3

    V, F, (s, h) = moulds.mould_half(P1R, step=0.2, pegs=False)
    cavity = s**2 * h - _closed_volume(V, F)
    pod = pg.mass_props(P1R, 1000)[0]
    assert abs(cavity - pod / 2) / (pod / 2) < 0.03


def test_rounded_rim_is_consistent_across_mass_mesh_fem_and_cover():
    vol_grid = pg.mass_props(P1R, 1000)[0]
    vol_mesh = _closed_volume(*pg.surface_mesh(P1R, n_theta=720, n_s=48))
    assert abs(vol_mesh - vol_grid) / vol_grid < 0.01
    assert 0.85 * pg.mass_props(P1, 1000)[0] < vol_grid < pg.mass_props(P1, 1000)[0]
    _, _, thick = pg.plane_mesh(P1R, *pg.FINE)
    assert thick.min() < 0.6 * P1R.t_edge / 1000  # FEM sees the thin rounded rim (element centres sit just inside the wall)
    assert pg.cover_depth(P1R) <= pg.cover_depth(P1)


def test_ga2_rules_for_hooking_and_narrowest_width():
    import ga2

    assert ga2.narrowest_width_mm(pg.Pod(25, 6, 8, 0, 0, 0, 1)) == pytest.approx(25, abs=0.01)
    # calipers bridge the valleys, so pick 1 reads 20.4 mm, more than its 19.1 mm valley-to-valley span
    assert ga2.narrowest_width_mm(P1) == pytest.approx(20.38, abs=0.05)
    assert ga2.narrowest_width_mm(P1) > 2 * (12.51 - 2.98)
    assert ga2.hooks_into_hole(pg.Pod(25, 10, 6, 0, 0, 0, 1))      # 10 mm hole, 6 mm thick: rings can link
    assert not ga2.hooks_into_hole(P1)                               # 6 mm hole, 7.7 mm thick, 6.5 mm wall


def test_ga2_smoke_run_writes_outputs(tmp_path):
    import ga2

    ga2.main(["--pop", "6", "--gens", "1", "--landings", "4", "--final-landings", "4", "--picks", "2",
              "--workers", "1", "--out", str(tmp_path)])
    for scen in ("A_tip_to_tip", "B_narrowest_25mm"):
        d = tmp_path / scen
        assert (d / "summary.md").exists() and (d / "pareto.csv").exists() and (d / "pareto.png").exists()
        assert len(list(d.glob("*_mould_half.stl"))) >= 1


def test_throw_stops_early_once_a_pod_has_clearly_rolled_away():
    import waves3d as w3

    smooth = pg.Pod(25.02, 6, 7.69, 0.2, 0, 0, 1)
    roll = dict(pos_tilt=np.pi / 2, v=(1.0, 0, 0), w=(0, 1.0 / 0.0125, 0))
    full = w3.throw(*pg.surface_mesh(smooth, 180, 12), **roll)
    capped = w3.throw(*pg.surface_mesh(smooth, 180, 12), max_dist=0.5, **roll)
    assert full["dist_m"] > 1.0
    assert 0.5 <= capped["dist_m"] < 0.6 and capped["t_s"] < full["t_s"] / 2


def test_throw_treats_a_pod_spinning_flat_in_place_as_settled():
    import waves3d as w3

    r = w3.throw(*pg.surface_mesh(P1R, 180, 12), pos_tilt=0.0, w=(0, 0, 40.0))  # flat, spinning like a top
    assert r["flat"] and r["dist_m"] < 0.005 and r["t_s"] < 0.5


def test_search_counts_a_pod_still_moving_at_the_time_limit_as_rolled_away():
    import ga2

    runs = [{"dist_m": 0.10, "flat": True, "t_s": 0.6},   # settled
            {"dist_m": 0.30, "flat": False, "t_s": 2.0},  # still rocking at the limit
            {"dist_m": 0.05, "flat": False, "t_s": 0.9}]  # settled on its edge
    d, edge = ga2.travel_and_edge(runs, t_max=2.0, cap_m=1.0)
    assert list(d) == [10.0, 100.0, 5.0]
    assert edge == pytest.approx(100 / 3)


def test_squeeze_loads_every_lobe_tip_touching_the_board():
    # A 5-lobe pod touches the top board at two tips (one at the bottom). The load must be shared
    # by both, mirror-symmetric, or the model bends the pod and reports it far too weak.
    pod = pg.Pod(27.39, 0, 6.85, 1.1, 5, 2.83, 1.02, 3.45)
    nodes, _, _ = pg.plane_mesh(pod, *pg.FINE)
    top = pg.board_nodes(nodes, top=True)
    assert abs(nodes[top, 0].sum()) < 1e-4 and (nodes[top, 0] > 0).any() and (nodes[top, 0] < 0).any()
    assert abs(nodes[pg.board_nodes(nodes, top=False), 0].sum()) < 1e-4
    # the solid disc is clearly stronger than the same outline with a hole. Only ~2.5x, not the ~10x of a
    # 4-lobe pod: one tip below and two above load it in three-point bending, where a central hole matters less
    ring = pg.Pod(27.39, 6, 6.85, 1.1, 5, 2.83, 1.02, 3.45)
    assert pg.squeeze_stress(pod) < pg.squeeze_stress(ring) / 2


def test_print_moulds_leave_size_margin_after_drying():
    import mix_compare as mc
    small = pg.Pod(25.09, 6, 6.15, 0, 4, 2.99, 0.98, 3.4)
    dried, mould = mc.print_scale(small, 26.0, 0.05)
    assert dried.D == pytest.approx(26.0) and mould.D == pytest.approx(26.0 / 0.95)
    assert dried.t_edge / small.t_edge == pytest.approx(26.0 / 25.09)       # scaled in every direction
    assert (dried.n, dried.p) == (small.n, small.p)
    big = pg.Pod(27.59, 6, 6.09, 0, 5, 2.99, 0.94, 3.42)                   # already over the margin: only shrink
    assert mc.print_scale(big, 26.0, 0.05)[0] == big
