"""台に固定された壁 D での小球と台の衝突を可視化する。"""

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
RESTITUTION = 0.65
BALL_SPEED_C = sqrt(2 * MASS_PLATFORM * GRAVITY * H1 / (MASS_PLATFORM + MASS_BALL))
PLATFORM_SPEED_C = MASS_BALL / MASS_PLATFORM * BALL_SPEED_C
ARRIVAL_TIME = CD_LENGTH / (BALL_SPEED_C + PLATFORM_SPEED_C)
BALL_SPEED_D = RESTITUTION * BALL_SPEED_C
PLATFORM_SPEED_D = RESTITUTION * PLATFORM_SPEED_C
POST_COLLISION_TIME = ARRIVAL_TIME * 0.85
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
    impact_x = CURVE_WIDTH + BALL_SPEED_C * ARRIVAL_TIME
    impact_platform_x = -PLATFORM_SPEED_C * ARRIVAL_TIME
    final_ball_x = impact_x - BALL_SPEED_D * POST_COLLISION_TIME
    final_platform_x = impact_platform_x + PLATFORM_SPEED_D * POST_COLLISION_TIME

    figure, axis = plt.subplots(figsize=(11, 6))
    figure.suptitle("Collision of the ball with the wall at D")
    axis.axhline(-0.45, color="#334155", linewidth=3)
    axis.text(2.0, -0.8, "smooth horizontal floor", color="#334155")
    axis.set_xlim(min(impact_platform_x, final_platform_x, final_ball_x) - 1.0, impact_x + 1.2)
    axis.set_ylim(-1.1, H2 + 1.0)
    axis.set_aspect("equal")
    axis.set_title("(4) Collision at the wall fixed to the platform")
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
    impact_mark, = axis.plot([], [], marker="*", color="#f59e0b", markersize=18)
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
        if frame <= 100:
            time = ARRIVAL_TIME * frame / 100
            platform_x = -PLATFORM_SPEED_C * time
            ball_x = CURVE_WIDTH + BALL_SPEED_C * time
            ball_velocity = BALL_SPEED_C
            platform_velocity = -PLATFORM_SPEED_C
            phase_text = (
                f"before collision: t = {time:.3f} s\n"
                f"ball = {BALL_SPEED_C:.2f} m/s right\n"
                f"platform = {PLATFORM_SPEED_C:.2f} m/s left"
            )
            impact_mark.set_data([], [])
        elif frame == 101:
            platform_x = impact_platform_x
            ball_x = impact_x
            ball_velocity = 0.0
            platform_velocity = 0.0
            phase_text = "collision at D\nrelative separation speed becomes e times approach speed"
            impact_mark.set_data([impact_x], [0])
        else:
            time = POST_COLLISION_TIME * (frame - 101) / 100
            platform_x = impact_platform_x + PLATFORM_SPEED_D * time
            ball_x = impact_x - BALL_SPEED_D * time
            ball_velocity = -BALL_SPEED_D
            platform_velocity = PLATFORM_SPEED_D
            phase_text = (
                f"after collision: t = {time:.3f} s\n"
                f"ball = {BALL_SPEED_D:.2f} m/s left\n"
                f"platform = {PLATFORM_SPEED_D:.2f} m/s right"
            )
            impact_mark.set_data([], [])

        wall_x = platform_x + CURVE_WIDTH + CD_LENGTH
        curve_track.set_data(
            [platform_x + point[0] for point in curve],
            [point[1] for point in curve],
        )
        horizontal_track.set_data((platform_x + CURVE_WIDTH, wall_x), (0, 0))
        wall_track.set_data((wall_x, wall_x), (0, 1.25))
        label_c.set_position((platform_x + CURVE_WIDTH - 0.05, 0.18))
        label_d.set_position((wall_x - 0.05, 1.38))
        ball.set_data([ball_x], [0])
        ball_arrow.set_positions(
            (ball_x, 0.22),
            (ball_x + ball_velocity * VECTOR_SCALE, 0.22),
        )
        platform_arrow.set_positions(
            (platform_x + CURVE_WIDTH + 0.65, -0.16),
            (platform_x + CURVE_WIDTH + 0.65 + platform_velocity * VECTOR_SCALE, -0.16),
        )
        info.set_text(
            f"{phase_text}\n"
            f"vD = e vC = {BALL_SPEED_D:.2f} m/s\n"
            f"VD = e VC = {PLATFORM_SPEED_D:.2f} m/s"
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
            impact_mark,
            info,
        )

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(202),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._collision_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
