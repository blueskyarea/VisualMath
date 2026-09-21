"""高さ h からの水平投射と、床に達する直前の速度成分を可視化する。"""

from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


HEIGHT = 5.0
HORIZONTAL_SPEED = 6.0
GRAVITY = 9.8
IMPACT_TIME = sqrt(2 * HEIGHT / GRAVITY)
IMPACT_VERTICAL_SPEED = -sqrt(2 * GRAVITY * HEIGHT)
IMPACT_X = HORIZONTAL_SPEED * IMPACT_TIME
VECTOR_SCALE = 0.10


def add_arrow(axis, color):
    arrow = FancyArrowPatch(
        (0, 0),
        (0, 0),
        arrowstyle="->",
        mutation_scale=14,
        linewidth=2.3,
        color=color,
    )
    axis.add_patch(arrow)
    return arrow


def set_arrow(arrow, start, vector):
    arrow.set_positions(start, (start[0] + vector[0], start[1] + vector[1]))


def main(interval_ms=70):
    frame_count = 100
    times = [IMPACT_TIME * index / frame_count for index in range(frame_count + 1)]
    x_values = [HORIZONTAL_SPEED * time for time in times]
    y_values = [-GRAVITY * time**2 / 2 for time in times]
    vy_values = [-GRAVITY * time for time in times]

    figure, (motion_axis, velocity_axis) = plt.subplots(1, 2, figsize=(13, 6))
    figure.suptitle("Horizontal projectile motion from height h")

    # 左: 地面から見た放物運動
    motion_axis.axhline(-HEIGHT, color="#334155", linewidth=3)
    motion_axis.axvline(0, color="#9ca3af", linewidth=1)
    motion_axis.plot(0, 0, marker="o", color="#111827")
    motion_axis.text(-0.35, 0.35, "launch point")
    motion_axis.plot(IMPACT_X, -HEIGHT, marker="x", color="#dc2626", markersize=10, mew=3)
    motion_axis.text(IMPACT_X - 0.5, -HEIGHT - 0.75, "floor")
    motion_axis.plot(x_values, y_values, color="#bfdbfe", linestyle="--")
    motion_axis.set_xlim(-0.8, IMPACT_X + 2.2)
    motion_axis.set_ylim(-HEIGHT - 1.3, 1.5)
    motion_axis.set_aspect("equal")
    motion_axis.set_title("Trajectory")
    motion_axis.set_xlabel("x (horizontal)")
    motion_axis.set_ylabel("y (upward positive)")
    motion_axis.grid(alpha=0.2)
    ball, = motion_axis.plot([], [], marker="o", color="#2563eb", markersize=9)
    trail, = motion_axis.plot([], [], color="#2563eb", linewidth=2)
    velocity_arrow = add_arrow(motion_axis, "#dc2626")
    motion_info = motion_axis.text(
        0.03,
        0.96,
        "",
        transform=motion_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # 右: 速度成分の時間変化
    velocity_axis.plot(times, [HORIZONTAL_SPEED] * len(times), color="#2563eb", label="vx = v")
    velocity_axis.plot(times, vy_values, color="#dc2626", label="vy = -gt")
    velocity_axis.axvline(IMPACT_TIME, color="#334155", linestyle="--")
    velocity_axis.set_title("Velocity components")
    velocity_axis.set_xlabel("time t [s]")
    velocity_axis.set_ylabel("velocity")
    velocity_axis.grid(alpha=0.2)
    velocity_axis.legend()
    vx_point, = velocity_axis.plot([], [], marker="o", color="#2563eb", markersize=7)
    vy_point, = velocity_axis.plot([], [], marker="o", color="#dc2626", markersize=7)
    velocity_info = velocity_axis.text(
        0.03,
        0.95,
        "",
        transform=velocity_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = times[frame]
        x = x_values[frame]
        y = y_values[frame]
        vy = vy_values[frame]
        ball.set_data([x], [y])
        trail.set_data(x_values[: frame + 1], y_values[: frame + 1])
        set_arrow(
            velocity_arrow,
            (x, y),
            (HORIZONTAL_SPEED * VECTOR_SCALE, vy * VECTOR_SCALE),
        )
        vx_point.set_data([time], [HORIZONTAL_SPEED])
        vy_point.set_data([time], [vy])
        motion_info.set_text(
            f"t = {time:.2f} / {IMPACT_TIME:.2f} s\n"
            f"x = {x:.2f}\n"
            f"y = {y:.2f}\n"
            "red arrow: velocity"
        )
        velocity_info.set_text(
            "at impact:\n"
            f"vx = v = {HORIZONTAL_SPEED:.2f}\n"
            f"vy = -sqrt(2gh) = {IMPACT_VERTICAL_SPEED:.2f}"
        )
        return ball, trail, velocity_arrow, motion_info, vx_point, vy_point, velocity_info

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(frame_count + 1),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._horizontal_projectile_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
