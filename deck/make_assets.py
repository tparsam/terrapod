# /// script
# requires-python = ">=3.10,<3.12"
# dependencies = ["numpy", "scipy", "matplotlib", "pymoo>=0.6", "mujoco<3.3"]
# ///
"""Renders the two final pods (as dried, 26 mm) for the deck, shaded in the deck palette, transparent PNG.

    uv run --python 3.11 deck/make_assets.py      -> deck/assets/*.png
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "geometry"))
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

import mix_compare as mc  # noqa: E402
import pod_ga as pg  # noqa: E402

OUT = Path(__file__).parent / "assets"
DARK, LIGHT = np.array(to_rgb("#273326")), np.array(to_rgb("#b9e1bf"))  # forest -> mint
PODS = {
    "pod_mixA_ring": ("ga2_mixA", "A_tip_to_tip", False),
    "pod_mixB_disc": ("ga2_mixB", "A_tip_to_tip", True),
}


def render(pod, path, elev, azim):
    V, F = pg.surface_mesh(pod, n_theta=360, n_s=32)
    tri = V[F] * 1000
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    light = np.array([-0.4, -0.5, 1.0])
    shade = np.clip(n @ (light / np.linalg.norm(light)), 0, 1)[:, None] ** 0.8
    fig = plt.figure(figsize=(8, 8), dpi=250)
    ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(Poly3DCollection(tri, facecolors=DARK + (LIGHT - DARK) * shade, edgecolors="none"))
    r = pod.D / 2
    ax.set(xlim=(-r, r), ylim=(-r, r), zlim=(-r, r))
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(path, transparent=True)
    plt.close(fig)
    img = plt.imread(path)  # crop to the pod, with a small margin
    ys, xs = np.nonzero(img[..., 3] > 0)
    m = 20
    plt.imsave(path, img[max(ys.min() - m, 0):ys.max() + m, max(xs.min() - m, 0):xs.max() + m])


def main():
    OUT.mkdir(exist_ok=True)
    for name, (folder, scen, disc) in PODS.items():
        pod = mc.pick1(mc.OUT / folder / scen)
        if disc:
            pod = pg.Pod(*[0.0 if k == "hole" else v for k, v in vars(pod).items()])
        dried, _ = mc.print_scale(pod, 26.0, 0.05)
        render(dried, OUT / f"{name}_angle.png", elev=35, azim=-60)
        render(dried, OUT / f"{name}_top.png", elev=90, azim=-90)
        print(name, f"D {dried.D:.1f} mm, thick {dried.t_edge + 2 * dried.dome:.1f} mm")


if __name__ == "__main__":
    main()
