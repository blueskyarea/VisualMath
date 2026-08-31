"""壁と床の間で静止する棒の力と摩擦条件を可視化する。"""

from math import cos, pi, sin, tan

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


MASS_ROD = 10.0
MASS_LOAD = 5.0
LENGTH = 4.0
ANGLE = pi / 3  # 60 deg
GRAVITY = 9.8


def add_arrow(axis, color):
    arrow = FancyArrowPatch(
        (0, 0),
        (0, 0),
        arrowstyle="->",
        mutation_scale=14,
        linewidth=2.2,
        color=color,
    )
    label = axis.text(0, 0, "", color=color, fontsize=8.5, va="center")
    axis.add_patch(arrow)
    return arrow, label


def set_arrow(item, start, end, label):
    arrow, text = item
    arrow.set_positions(start, end)
    text.set_position((end[0] + 0.08, end[1] + 0.08))
    text.set_text(label)


def setup_fbd(axis, title):
    base = (0.0, 0.0)
    top = (LENGTH * cos(ANGLE), LENGTH * sin(ANGLE))
    axis.axhline(0, color="#475569", linewidth=3)
    axis.plot((top[0], top[0]), (0, top[1] + 1), color="#475569", linewidth=3)
    axis.plot((base[0], top[0]), (base[1], top[1]), color="#111827", linewidth=6)
    axis.text(-0.25, -0.35, "A")
    axis.text(top[0] + 0.12, top[1] + 0.1, "B")
    axis.text(top[0] - 0.6, 0.3, "wall")
    axis.set_xlim(-1.2, top[0] + 2.2)
    axis.set_ylim(-1.2, top[1] + 1.5)
    axis.set_aspect("equal")
    axis.set_title(title)
    axis.axis("off")
    return base, top


def main(interval_ms=70):
    figure, axes = plt.subplots(2, 2, figsize=(13, 10))
    figure.suptitle("Static equilibrium of a rod between a wall and a floor")
    fbd_1_axis, mu_1_axis, fbd_3_axis, mu_3_axis = axes.flat
    base, top = setup_fbd(fbd_1_axis, "(1) Forces on the rod")
    setup_fbd(fbd_3_axis, "(3) Forces with a hanging mass")

    center = (top[0] / 2, top[1] / 2)
    normal_1 = add_arrow(fbd_1_axis, "#2563eb")
    friction_1 = add_arrow(fbd_1_axis, "#16a34a")
    wall_1 = add_arrow(fbd_1_axis, "#7c3aed")
    weight_1 = add_arrow(fbd_1_axis, "#dc2626")
    normal_force_1 = MASS_ROD * GRAVITY
    friction_force_1 = MASS_ROD * GRAVITY / (2 * tan(ANGLE))
    set_arrow(normal_1, base, (base[0], base[1] + 1.2), "N = Mg")
    set_arrow(friction_1, base, (base[0] + 1.2, base[1]), "f")
    set_arrow(wall_1, top, (top[0] - 1.2, top[1]), "wall force")
    set_arrow(weight_1, center, (center[0], center[1] - 1.0), "Mg")
    fbd_1_axis.text(
        0.03,
        0.04,
        f"N = {normal_force_1:.1f} N\nf = Mg/(2 tan theta) = {friction_force_1:.1f} N",
        transform=fbd_1_axis.transAxes,
        va="bottom",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # (2) theta に対する必要最小摩擦係数
    theta_values = list(range(10, 86))
    mu_1_values = [1 / (2 * tan(value * pi / 180)) for value in theta_values]
    mu_1_min = 1 / (2 * tan(ANGLE))
    mu_1_axis.plot(theta_values, mu_1_values, color="#64748b")
    mu_1_axis.axvline(60, color="#dc2626", linestyle="--")
    mu_1_axis.set_title("(2) Condition on static friction")
    mu_1_axis.set_xlabel("theta [deg]")
    mu_1_axis.set_ylabel("minimum mu")
    mu_1_axis.grid(alpha=0.2)
    mu_1_axis.plot(60, mu_1_min, marker="o", color="#dc2626")
    mu_1_axis.text(
        0.04,
        0.95,
        "mu >= 1 / (2 tan theta)\n"
        f"at theta = 60 deg: mu >= {mu_1_min:.3f}",
        transform=mu_1_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # (3) おもりの位置に応じて更新する自由物体図
    normal_3 = add_arrow(fbd_3_axis, "#2563eb")
    friction_3 = add_arrow(fbd_3_axis, "#16a34a")
    wall_3 = add_arrow(fbd_3_axis, "#7c3aed")
    rod_weight_3 = add_arrow(fbd_3_axis, "#dc2626")
    load_weight_3 = add_arrow(fbd_3_axis, "#f59e0b")
    load_marker, = fbd_3_axis.plot([], [], marker="o", color="#f59e0b", markersize=8)
    fbd_3_info = fbd_3_axis.text(
        0.03,
        0.04,
        "",
        transform=fbd_3_axis.transAxes,
        va="bottom",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # (4) x/L に対する必要最小摩擦係数
    ratios = [index / 100 for index in range(101)]
    mu_3_values = [
        (MASS_ROD / 2 + MASS_LOAD * (1 - ratio))
        / ((MASS_ROD + MASS_LOAD) * tan(ANGLE))
        for ratio in ratios
    ]
    mu_3_axis.plot(ratios, mu_3_values, color="#64748b")
    mu_3_axis.set_title("(4) Condition with a hanging mass")
    mu_3_axis.set_xlabel("x / L  (distance from B)")
    mu_3_axis.set_ylabel("minimum mu")
    mu_3_axis.grid(alpha=0.2)
    mu_3_point, = mu_3_axis.plot([], [], marker="o", color="#dc2626")
    mu_3_info = mu_3_axis.text(
        0.03,
        0.95,
        "",
        transform=mu_3_axis.transAxes,
        va="top",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        ratio = ratios[frame]
        x_from_b = ratio * LENGTH
        distance_from_a = LENGTH - x_from_b
        load_position = (
            distance_from_a * cos(ANGLE),
            distance_from_a * sin(ANGLE),
        )
        normal_force = (MASS_ROD + MASS_LOAD) * GRAVITY
        friction_force = GRAVITY * (
            MASS_ROD / 2 + MASS_LOAD * (1 - ratio)
        ) / tan(ANGLE)
        minimum_mu = friction_force / normal_force

        set_arrow(normal_3, base, (base[0], base[1] + 1.2), "N")
        set_arrow(friction_3, base, (base[0] + 1.2, base[1]), "f")
        set_arrow(wall_3, top, (top[0] - 1.2, top[1]), "wall force")
        set_arrow(rod_weight_3, center, (center[0], center[1] - 1.0), "Mg")
        set_arrow(load_weight_3, load_position, (load_position[0], load_position[1] - 0.9), "mg")
        load_marker.set_data([load_position[0]], [load_position[1]])
        fbd_3_info.set_text(
            f"x/L = {ratio:.2f}\n"
            f"N = (M + m)g = {normal_force:.1f} N\n"
            f"f = {friction_force:.1f} N"
        )
        mu_3_point.set_data([ratio], [minimum_mu])
        mu_3_info.set_text(
            "mu >= [M/2 + m(1 - x/L)]\n"
            "/ [(M + m) tan theta]\n"
            f"mu >= {minimum_mu:.3f}"
        )
        return (
            normal_3[0], normal_3[1],
            friction_3[0], friction_3[1],
            wall_3[0], wall_3[1],
            rod_weight_3[0], rod_weight_3[1],
            load_weight_3[0], load_weight_3[1],
            load_marker, fbd_3_info, mu_3_point, mu_3_info,
        )

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(len(ratios)),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._ladder_equilibrium_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
