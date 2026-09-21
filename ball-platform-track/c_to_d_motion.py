"""小球が C から台に固定された壁 D へ至る相対運動を可視化する。"""

from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


MASS_PLATFORM = 1.4
MASS_BALL = 0.60
GRAVITY = 9.8
H1 = 4.0
H2 = 2.0
CURVE_WIDTH = 2.2
CD_LENGTH = 3.5
BALL_SPEED_C = sqrt(2 * MASS_PLATFORM * GRAVITY * H1 / (MASS_PLATFORM + MASS_BALL))
PLATFORM_SPEED_C = MASS_BALL / MASS_PLATFORM * BALL_SPEED_C
RELATIVE_SPEED = BALL_SPEED_C + PLATFORM_SPEED_C
ARRIVAL_TIME = CD_LENGTH / RELATIVE_SPEED
VECTOR_SCALE = 0.16


def curve_position(u):
    """B-C の曲線を台に固定した座標で表す。"""
    x = 3 * (1 - u) * u**2 * CURVE_WIDTH * 0.65 + u**3 * CURVE_WIDTH
    y = (1 - u) ** 3 * H2 + 3 * (1 - u) ** 2 * u * (H2 / 2)
    return x, y


def add_arrow(axis, color):
    arrow = FancyArrowPatch(
        (0, 0),
        (0, 0),
        arrowstyle="->",
        mutation_scale=14,
        linewidth=2.2,
        color=color,
    )
    axis.add_patch(arrow)
    return arrow


def main(interval_ms=60):
    curve = [curve_position(index / 100) for index in range(101)]
    figure, axis = plt.subplots(figsize=(11, 6))
    figure.suptitle("Ball motion from C to the moving wall D")

    platform_shift = PLATFORM_SPEED_C * ARRIVAL_TIME
    axis.axhline(-0.45, color="#334155", linewidth=3)
    axis.text(2.0, -0.8, "smooth horizontal floor", color="#334155")
    axis.set_xlim(-platform_shift - 1.0, CURVE_WIDTH + CD_LENGTH + 1.0)
    axis.set_ylim(-1.1, H2 + 1.0)
    axis.set_aspect("equal")
    axis.set_title("(3) Ball approaching a wall fixed to the platform")
    axis.set_xlabel("horizontal direction")
    axis.set_ylabel("vertical direction")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.grid(alpha=0.15)

    curve_track, = axis.plot([], [], color="#475569", linewidth=5)
    horizontal_track, = axis.plot([], [], color="#475569", linewidth=5)
    wall_track, = axis.plot([], [], color="#7c2d12", linewidth=5)
    label_c = axis.text(0, 0, "C")
    label_d = axis.text(0, 0, "D")
    ball, = axis.plot([], [], marker="o", color="#2563eb", markersize=10)
    ball_arrow = add_arrow(axis, "#dc2626")
    platform_arrow = add_arrow(axis, "#16a34a")
    approach_arrow = add_arrow(axis, "#7c3aed")
    info = axis.text(
        0.03,
        0.95,
        "",
        transform=axis.transAxes,
        va="top",
        fontsize=9.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = ARRIVAL_TIME * frame / 120
        platform_x = -PLATFORM_SPEED_C * time
        ball_x = CURVE_WIDTH + BALL_SPEED_C * time
        wall_x = platform_x + CURVE_WIDTH + CD_LENGTH
        collision = frame == 120

        curve_track.set_data(
            [platform_x + point[0] for point in curve],
            [point[1] for point in curve],
        )
        horizontal_track.set_data(
            (platform_x + CURVE_WIDTH, wall_x), (0, 0))
        wall_track.set_data((wall_x, wall_x), (0, 1.25))
        label_c.set_position((platform_x + CURVE_WIDTH - 0.05, 0.18))
        label_d.set_position((wall_x - 0.05, 1.38))
        ball.set_data([ball_x], [0])
        ball.set_color("#dc2626" if collision else "#2563eb")
        ball_arrow.set_positions(
            (ball_x, 0.22),
            (ball_x + BALL_SPEED_C * VECTOR_SCALE, 0.22),
        )
        platform_arrow.set_positions(
            (platform_x + CURVE_WIDTH + 0.65, -0.16),
            (platform_x + CURVE_WIDTH + 0.65 - PLATFORM_SPEED_C * VECTOR_SCALE, -0.16),
        )
        midpoint = (ball_x + wall_x) / 2
        approach_arrow.set_positions((midpoint - 0.35, 0.75), (midpoint + 0.35, 0.75))
        info.set_text(
            f"time after C = {time:.3f} s\n"
            f"ball: {BALL_SPEED_C:.2f} m/s right\n"
            f"platform and wall: {PLATFORM_SPEED_C:.2f} m/s left\n"
            f"approach speed = vC + VC = {RELATIVE_SPEED:.2f} m/s\n"
            f"arrival time = a / (vC + VC) = {ARRIVAL_TIME:.3f} s"
        )
        return (
            curve_track,
            horizontal_track,
            wall_track,
            label_c,
            label_d,
            ball,
            ball_arrow,
            platform_arrow,
            approach_arrow,
            info,
        )

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(121),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._c_to_d_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
