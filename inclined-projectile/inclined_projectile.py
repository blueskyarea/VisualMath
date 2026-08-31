"""斜面から投げた小球の、斜面座標での運動を可視化する。"""

from math import cos, pi, sin

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


GRAVITY = 9.8
SPEED = 10.0
INCLINE_ANGLE = pi / 6
LAUNCH_ANGLE = pi / 6
IMPACT_TIME = 2 * SPEED * sin(LAUNCH_ANGLE) / (GRAVITY * cos(INCLINE_ANGLE))
RANGE_ON_SLOPE = 2 * SPEED**2 / (3 * GRAVITY)


def velocity_x(time):
    return SPEED * cos(LAUNCH_ANGLE) - GRAVITY * sin(INCLINE_ANGLE) * time


def velocity_y(time):
    return SPEED * sin(LAUNCH_ANGLE) - GRAVITY * cos(INCLINE_ANGLE) * time


def position_x(time):
    return SPEED * cos(LAUNCH_ANGLE) * time - GRAVITY * sin(INCLINE_ANGLE) * time**2 / 2


def position_y(time):
    return SPEED * sin(LAUNCH_ANGLE) * time - GRAVITY * cos(INCLINE_ANGLE) * time**2 / 2


def to_ground_coordinates(x, y):
    """斜面座標 (x, y) を水平・鉛直座標へ変換する。"""
    return (
        x * cos(INCLINE_ANGLE) - y * sin(INCLINE_ANGLE),
        x * sin(INCLINE_ANGLE) + y * cos(INCLINE_ANGLE),
    )


def main(interval_ms=80):
    frame_count = 100
    times = [IMPACT_TIME * index / frame_count for index in range(frame_count + 1)]
    vx_values = [velocity_x(time) for time in times]
    vy_values = [velocity_y(time) for time in times]
    x_values = [position_x(time) for time in times]
    y_values = [position_y(time) for time in times]
    ground_path = [to_ground_coordinates(x, y) for x, y in zip(x_values, y_values)]
    impact_ground = to_ground_coordinates(RANGE_ON_SLOPE, 0)

    figure, axes = plt.subplots(2, 2, figsize=(13, 10))
    figure.suptitle("Projectile motion on a 30-degree incline")
    velocity_axis, position_axis, impact_axis, scene_axis = axes.flat

    # (1) 速度成分
    velocity_axis.plot(times, vx_values, color="#2563eb", label="vx")
    velocity_axis.plot(times, vy_values, color="#16a34a", label="vy")
    velocity_axis.axhline(0, color="#9ca3af", linewidth=1)
    velocity_axis.set_title("(1) Velocity components")
    velocity_axis.set_xlabel("time t [s]")
    velocity_axis.set_ylabel("velocity")
    velocity_axis.grid(alpha=0.2)
    velocity_axis.legend()
    vx_point, = velocity_axis.plot([], [], marker="o", color="#2563eb")
    vy_point, = velocity_axis.plot([], [], marker="o", color="#16a34a")
    velocity_info = velocity_axis.text(
        0.03,
        0.95,
        "",
        transform=velocity_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # (2) 斜面座標での位置
    position_axis.plot(times, x_values, color="#2563eb", label="x: along slope")
    position_axis.plot(times, y_values, color="#16a34a", label="y: normal to slope")
    position_axis.axhline(0, color="#9ca3af", linewidth=1)
    position_axis.set_title("(2) Position in slope coordinates")
    position_axis.set_xlabel("time t [s]")
    position_axis.set_ylabel("position")
    position_axis.grid(alpha=0.2)
    position_axis.legend()
    x_point, = position_axis.plot([], [], marker="o", color="#2563eb")
    y_point, = position_axis.plot([], [], marker="o", color="#16a34a")
    position_info = position_axis.text(
        0.03,
        0.95,
        "",
        transform=position_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # (3) y=0 となる衝突時刻
    impact_axis.plot(times, y_values, color="#16a34a", linewidth=2)
    impact_axis.axhline(0, color="#334155", linewidth=1.5)
    impact_axis.axvline(IMPACT_TIME, color="#dc2626", linestyle="--")
    impact_axis.set_title("(3) Impact occurs when y = 0")
    impact_axis.set_xlabel("time t [s]")
    impact_axis.set_ylabel("normal position y")
    impact_axis.grid(alpha=0.2)
    impact_point, = impact_axis.plot([], [], marker="o", color="#dc2626")
    impact_info = impact_axis.text(
        0.03,
        0.95,
        "",
        transform=impact_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # (4) 水平・鉛直方向から見た実際の軌跡
    slope_x = [-1, impact_ground[0] + 3]
    slope_y = [value * sin(INCLINE_ANGLE) / cos(INCLINE_ANGLE) for value in slope_x]
    scene_axis.plot(slope_x, slope_y, color="#475569", linewidth=3)
    scene_axis.plot(0, 0, marker="o", color="#111827")
    scene_axis.text(-0.5, -0.9, "O")
    scene_axis.plot(impact_ground[0], impact_ground[1], marker="x", color="#dc2626", markersize=10, mew=3)
    scene_axis.text(impact_ground[0] + 0.35, impact_ground[1] + 0.25, "P")
    scene_axis.plot(
        [point[0] for point in ground_path],
        [point[1] for point in ground_path],
        color="#bfdbfe",
        linestyle="--",
    )
    scene_axis.set_xlim(-1.5, impact_ground[0] + 3.5)
    scene_axis.set_ylim(-1.5, max(point[1] for point in ground_path) + 2)
    scene_axis.set_aspect("equal")
    scene_axis.set_title("(4) Trajectory and distance OP")
    scene_axis.set_xlabel("horizontal position")
    scene_axis.set_ylabel("vertical position")
    scene_axis.grid(alpha=0.2)
    ball, = scene_axis.plot([], [], marker="o", color="#2563eb", markersize=8)
    trail, = scene_axis.plot([], [], color="#2563eb", linewidth=2)
    scene_info = scene_axis.text(
        0.03,
        0.95,
        "",
        transform=scene_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = times[frame]
        x = x_values[frame]
        y = y_values[frame]
        ground_x, ground_y = ground_path[frame]
        vx_point.set_data([time], [vx_values[frame]])
        vy_point.set_data([time], [vy_values[frame]])
        x_point.set_data([time], [x])
        y_point.set_data([time], [y])
        impact_point.set_data([time], [y])
        ball.set_data([ground_x], [ground_y])
        trail.set_data(
            [point[0] for point in ground_path[: frame + 1]],
            [point[1] for point in ground_path[: frame + 1]],
        )
        velocity_info.set_text(
            "vx = (sqrt(3)/2)V - (1/2)gt\n"
            "vy = (1/2)V - (sqrt(3)/2)gt"
        )
        position_info.set_text(
            "x = (sqrt(3)/2)Vt - (1/4)gt^2\n"
            "y = (1/2)Vt - (sqrt(3)/4)gt^2"
        )
        impact_info.set_text(
            f"t = {time:.2f} s\n"
            f"impact time = 2V/(sqrt(3)g)\n"
            f"= {IMPACT_TIME:.2f} s"
        )
        scene_info.set_text(
            f"OP = 2V^2/(3g)\n"
            f"= {RANGE_ON_SLOPE:.2f} (along slope)"
        )
        return (
            vx_point,
            vy_point,
            velocity_info,
            x_point,
            y_point,
            position_info,
            impact_point,
            impact_info,
            ball,
            trail,
            scene_info,
        )

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
    figure._inclined_projectile_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
