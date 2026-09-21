"""壁 D で反発した小球が B を越えて最高点へ至る運動を可視化する。"""

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
RESTITUTION = 0.80  # e^2 h1 = 2.56 m > h2, so the ball passes B.
H3 = RESTITUTION**2 * H1
BALL_SPEED_C = sqrt(2 * MASS_PLATFORM * GRAVITY * H1 / (MASS_PLATFORM + MASS_BALL))
PLATFORM_SPEED_C = MASS_BALL / MASS_PLATFORM * BALL_SPEED_C
BALL_SPEED_D = RESTITUTION * BALL_SPEED_C
PLATFORM_SPEED_D = RESTITUTION * PLATFORM_SPEED_C
TIME_C_TO_D = CD_LENGTH / (BALL_SPEED_C + PLATFORM_SPEED_C)
TIME_D_TO_C = CD_LENGTH / (BALL_SPEED_D + PLATFORM_SPEED_D)
VECTOR_SCALE = 0.14


def curve_position(u):
    """B-C の曲線を、台に固定した座標で表す。"""
    x = 3 * (1 - u) * u**2 * CURVE_WIDTH * 0.65 + u**3 * CURVE_WIDTH
    y = (1 - u) ** 3 * H2 + 3 * (1 - u) ** 2 * u * (H2 / 2)
    return x, y


def curve_derivative(u):
    """曲線の u に関する微分を返す。"""
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


def reverse_curve_state(u):
    """反発後のエネルギー e^2*m*g*h1 で C から B へ戻る状態を求める。"""
    x, y = curve_position(u)
    dx_du, dy_du = curve_derivative(u)
    coefficient = (
        MASS_BALL * MASS_PLATFORM / (MASS_PLATFORM + MASS_BALL) * dx_du**2
        + MASS_BALL * dy_du**2
    )
    du_dt = -sqrt(2 * MASS_BALL * GRAVITY * (H3 - y) / coefficient)
    local_vx = dx_du * du_dt
    local_vy = dy_du * du_dt
    platform_shift = -MASS_BALL / (MASS_PLATFORM + MASS_BALL) * (x - CURVE_WIDTH)
    platform_vx = -MASS_BALL / (MASS_PLATFORM + MASS_BALL) * local_vx
    ball_shift = platform_shift + x - CURVE_WIDTH
    ball_vx = platform_vx + local_vx
    return platform_shift, ball_shift, y, platform_vx, ball_vx, local_vy, abs(du_dt)


def build_states():
    """D-C、C-B、B-最高点の各段階をつないだ状態列を作る。"""
    states = []
    impact_platform_x = -PLATFORM_SPEED_C * TIME_C_TO_D
    impact_ball_x = impact_platform_x + CURVE_WIDTH + CD_LENGTH

    # D-C: 小球は左、台と壁は右へ進む。
    for index in range(81):
        time = TIME_D_TO_C * index / 80
        platform_x = impact_platform_x + PLATFORM_SPEED_D * time
        ball_x = impact_ball_x - BALL_SPEED_D * time
        states.append((time, platform_x, ball_x, 0.0, PLATFORM_SPEED_D, -BALL_SPEED_D, 0.0, "D-C"))

    # C-B: 曲面上で、台は右向きに反動する。
    curve_time = TIME_D_TO_C
    previous_speed_u = reverse_curve_state(1.0)[-1]
    platform_at_c = states[-1][1]
    for index in range(1, 101):
        u = 1 - index / 100
        state = reverse_curve_state(u)
        speed_u = state[-1]
        curve_time += (1 / previous_speed_u + 1 / speed_u) / 200
        platform_shift, ball_shift, y, platform_vx, ball_vx, ball_vy, _ = state
        states.append(
            (
                curve_time,
                platform_at_c + platform_shift,
                platform_at_c + CURVE_WIDTH + ball_shift,
                y,
                platform_vx,
                ball_vx,
                ball_vy,
                "C-B",
            )
        )
        previous_speed_u = speed_u

    # B から上の鉛直部分では、台は水平に動かず、小球は鉛直上向きに進む。
    time_to_top = sqrt(2 * (H3 - H2) / GRAVITY)
    platform_at_b = states[-1][1]
    for index in range(1, 71):
        time = time_to_top * index / 70
        y = H2 + sqrt(2 * GRAVITY * (H3 - H2)) * time - GRAVITY * time**2 / 2
        states.append(
            (
                curve_time + time,
                platform_at_b,
                platform_at_b,
                y,
                0.0,
                0.0,
                sqrt(max(0.0, 2 * GRAVITY * (H3 - y))),
                "B-top",
            )
        )
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
    figure.suptitle("Ball returning from D, passing B, and reaching its highest point")
    axis.axhline(-0.45, color="#334155", linewidth=3)
    axis.text(2.0, -0.8, "smooth horizontal floor", color="#334155")
    axis.set_xlim(-2.3, CURVE_WIDTH + CD_LENGTH + 1.4)
    axis.set_ylim(-1.1, H1 + 1.0)
    axis.set_aspect("equal")
    axis.set_title("(5) From the rebound at D to the highest point")
    axis.set_xlabel("horizontal direction")
    axis.set_ylabel("vertical direction")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.grid(alpha=0.15)

    vertical_track, = axis.plot([], [], color="#475569", linewidth=5)
    curve_track, = axis.plot([], [], color="#475569", linewidth=5)
    horizontal_track, = axis.plot([], [], color="#475569", linewidth=5)
    wall_track, = axis.plot([], [], color="#7c2d12", linewidth=5)
    label_b = axis.text(0, 0, "B")
    label_c = axis.text(0, 0, "C")
    label_d = axis.text(0, 0, "D")
    ball, = axis.plot([], [], marker="o", color="#2563eb", markersize=10)
    ball_arrow = add_arrow(axis, "#dc2626")
    platform_arrow = add_arrow(axis, "#16a34a")
    top_line, = axis.plot([], [], color="#7c3aed", linestyle="--", linewidth=1.5)
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
        wall_x = platform_x + CURVE_WIDTH + CD_LENGTH
        vertical_track.set_data((platform_x, platform_x), (0, H1))
        curve_track.set_data(
            [platform_x + point[0] for point in curve],
            [point[1] for point in curve],
        )
        horizontal_track.set_data((platform_x + CURVE_WIDTH, wall_x), (0, 0))
        wall_track.set_data((wall_x, wall_x), (0, 1.25))
        label_b.set_position((platform_x - 0.3, H2 + 0.1))
        label_c.set_position((platform_x + CURVE_WIDTH - 0.05, 0.18))
        label_d.set_position((wall_x - 0.05, 1.38))
        ball.set_data([ball_x], [ball_y])
        ball_arrow.set_positions(
            (ball_x, ball_y),
            (ball_x + ball_vx * VECTOR_SCALE, ball_y + ball_vy * VECTOR_SCALE),
        )
        platform_arrow.set_positions(
            (platform_x + CURVE_WIDTH + 0.65, -0.16),
            (platform_x + CURVE_WIDTH + 0.65 + platform_vx * VECTOR_SCALE, -0.16),
        )
        top_line.set_data((platform_x - 0.55, platform_x + 0.55), (H3, H3))

        descriptions = {
            "D-C": "D to C: ball moves left; platform and wall move right",
            "C-B": "C to B: the ball climbs the curve and the platform slows down",
            "B-top": "above B: the ball rises vertically; the platform is at rest",
        }
        info.set_text(
            f"{descriptions[phase]}\n"
            f"time after rebound = {time:.2f} s\n"
            f"remaining energy = e^2 m g h1\n"
            f"highest point: h3 = e^2 h1 = {H3:.2f} m"
        )
        return (
            vertical_track,
            curve_track,
            horizontal_track,
            wall_track,
            label_b,
            label_c,
            label_d,
            ball,
            ball_arrow,
            platform_arrow,
            top_line,
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
    figure._return_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
