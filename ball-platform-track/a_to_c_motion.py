"""小球が A から曲面を通り C へ至る際の台の反動を可視化する。"""

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
HORIZONTAL_LENGTH = 3.5
VERTICAL_DROP_TIME = sqrt(2 * (H1 - H2) / GRAVITY)
BALL_SPEED_C = sqrt(2 * MASS_PLATFORM * GRAVITY * H1 / (MASS_PLATFORM + MASS_BALL))
PLATFORM_SPEED_C = MASS_BALL / MASS_PLATFORM * BALL_SPEED_C
VECTOR_SCALE = 0.13


def curve_position(u):
    """B-C の3次ベジェ曲線上の、台に対する位置を返す。"""
    x = 3 * (1 - u) * u**2 * CURVE_WIDTH * 0.65 + u**3 * CURVE_WIDTH
    y = (1 - u) ** 3 * H2 + 3 * (1 - u) ** 2 * u * (H2 / 2)
    return x, y


def curve_derivative(u):
    """B-C 曲線の u に関する微分を返す。"""
    p0 = (0.0, H2)
    p1 = (0.0, H2 / 2)
    p2 = (CURVE_WIDTH * 0.65, 0.0)
    p3 = (CURVE_WIDTH, 0.0)
    dx = (
        3 * (1 - u) ** 2 * (p1[0] - p0[0])
        + 6 * (1 - u) * u * (p2[0] - p1[0])
        + 3 * u**2 * (p3[0] - p2[0])
    )
    dy = (
        3 * (1 - u) ** 2 * (p1[1] - p0[1])
        + 6 * (1 - u) * u * (p2[1] - p1[1])
        + 3 * u**2 * (p3[1] - p2[1])
    )
    return dx, dy


def curve_state(u):
    """曲線上での位置と速度を、エネルギー・運動量保存から求める。"""
    x, y = curve_position(u)
    dx_du, dy_du = curve_derivative(u)
    coefficient = (
        MASS_BALL * MASS_PLATFORM / (MASS_PLATFORM + MASS_BALL) * dx_du**2
        + MASS_BALL * dy_du**2
    )
    du_dt = sqrt(2 * MASS_BALL * GRAVITY * (H1 - y) / coefficient)
    local_vx = dx_du * du_dt
    local_vy = dy_du * du_dt
    platform_x = -MASS_BALL / (MASS_PLATFORM + MASS_BALL) * x
    platform_vx = -MASS_BALL / (MASS_PLATFORM + MASS_BALL) * local_vx
    ball_x = platform_x + x
    ball_vx = platform_vx + local_vx
    return platform_x, ball_x, y, platform_vx, ball_vx, local_vy, du_dt


def build_states():
    states = []
    # A-B: 台も小球も水平方向には動かない。
    for index in range(71):
        time = VERTICAL_DROP_TIME * index / 70
        states.append((time, 0.0, 0.0, H1 - GRAVITY * time**2 / 2, 0.0, 0.0, -GRAVITY * time, "A-B"))

    # B-C: 曲線に沿う運動を小さな区間に分け、経過時間を積算する。
    curve_time = VERTICAL_DROP_TIME
    previous_u = 0.0
    previous_du_dt = curve_state(0.0)[-1]
    for index in range(1, 101):
        u = index / 100
        state = curve_state(u)
        current_du_dt = state[-1]
        du = u - previous_u
        curve_time += du * (1 / previous_du_dt + 1 / current_du_dt) / 2
        platform_x, ball_x, y, platform_vx, ball_vx, ball_vy, _ = state
        states.append((curve_time, platform_x, ball_x, y, platform_vx, ball_vx, ball_vy, "B-C"))
        previous_u = u
        previous_du_dt = current_du_dt
    return states


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
    states = build_states()
    curve = [curve_position(index / 100) for index in range(101)]
    figure, axis = plt.subplots(figsize=(11, 6))
    figure.suptitle("Ball and platform motion from A through B to C")

    axis.axhline(-0.45, color="#334155", linewidth=3)
    axis.text(2.0, -0.8, "smooth horizontal floor", color="#334155")
    axis.set_xlim(-1.7, CURVE_WIDTH + HORIZONTAL_LENGTH + 1.2)
    axis.set_ylim(-1.1, H1 + 1.0)
    axis.set_aspect("equal")
    axis.set_title("(2) Motion from A to C")
    axis.set_xlabel("horizontal direction")
    axis.set_ylabel("vertical direction")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.grid(alpha=0.15)

    vertical_track, = axis.plot([], [], color="#475569", linewidth=5)
    curve_track, = axis.plot([], [], color="#475569", linewidth=5)
    horizontal_track, = axis.plot([], [], color="#475569", linewidth=5)
    wall_track, = axis.plot([], [], color="#7c2d12", linewidth=5)
    label_a = axis.text(0, 0, "A")
    label_b = axis.text(0, 0, "B")
    label_c = axis.text(0, 0, "C")
    ball, = axis.plot([], [], marker="o", color="#2563eb", markersize=10)
    ball_arrow = add_arrow(axis, "#dc2626")
    platform_arrow = add_arrow(axis, "#16a34a")
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
        time, platform_x, ball_x, ball_y, platform_vx, ball_vx, ball_vy, phase = states[frame]
        vertical_track.set_data((platform_x, platform_x), (0, H1))
        curve_track.set_data(
            [platform_x + point[0] for point in curve],
            [point[1] for point in curve],
        )
        horizontal_track.set_data(
            (platform_x + CURVE_WIDTH, platform_x + CURVE_WIDTH + HORIZONTAL_LENGTH),
            (0, 0),
        )
        wall_x = platform_x + CURVE_WIDTH + HORIZONTAL_LENGTH
        wall_track.set_data((wall_x, wall_x), (0, 1.3))
        label_a.set_position((platform_x - 0.3, H1 + 0.1))
        label_b.set_position((platform_x - 0.3, H2 + 0.1))
        label_c.set_position((platform_x + CURVE_WIDTH - 0.05, 0.18))
        ball.set_data([ball_x], [ball_y])
        ball_arrow.set_positions(
            (ball_x, ball_y),
            (ball_x + ball_vx * VECTOR_SCALE, ball_y + ball_vy * VECTOR_SCALE),
        )
        platform_arrow.set_positions(
            (platform_x + CURVE_WIDTH + 0.6, -0.15),
            (platform_x + CURVE_WIDTH + 0.6 + platform_vx * VECTOR_SCALE, -0.15),
        )

        if phase == "A-B":
            info.set_text(
                f"A to B: t = {time:.2f} s\n"
                "platform speed = 0\n"
                "ball falls vertically"
            )
        else:
            info.set_text(
                f"B to C: t = {time:.2f} s\n"
                "the curved track pushes the platform left\n"
                f"at C: ball speed = {BALL_SPEED_C:.2f}\n"
                f"at C: platform speed = {PLATFORM_SPEED_C:.2f} (left)"
            )
        return (
            vertical_track,
            curve_track,
            horizontal_track,
            wall_track,
            label_a,
            label_b,
            label_c,
            ball,
            ball_arrow,
            platform_arrow,
            info,
        )

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(len(states)),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._a_to_c_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
