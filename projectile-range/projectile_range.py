"""同じ水平距離に届く投射角と初速度の関係を可視化する。"""

from math import cos, radians, sin, sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


GRAVITY = 9.8
RANGE = 20.0
ANGLES = (15, 25, 35, 45, 55, 65, 75)


def initial_speed(angle_degrees):
    """水平距離 RANGE に届くための初速度を返す。"""
    return sqrt(GRAVITY * RANGE / sin(2 * radians(angle_degrees)))


def trajectory(angle_degrees, points=100):
    """指定角度で投げたときの x, y 座標列を返す。"""
    angle = radians(angle_degrees)
    speed = initial_speed(angle_degrees)
    flight_time = 2 * speed * sin(angle) / GRAVITY
    times = [flight_time * index / points for index in range(points + 1)]
    return (
        [speed * cos(angle) * time for time in times],
        [speed * sin(angle) * time - GRAVITY * time**2 / 2 for time in times],
    )


def main(interval_ms=1300):
    trajectories = {angle: trajectory(angle) for angle in ANGLES}
    speeds = [initial_speed(angle) for angle in ANGLES]
    max_height = max(max(y_values) for _, y_values in trajectories.values())
    min_speed = sqrt(GRAVITY * RANGE)

    figure, (path_axis, speed_axis) = plt.subplots(1, 2, figsize=(13, 6))
    figure.suptitle("Projectile motion: reaching the same horizontal range")

    path_axis.axhline(0, color="#334155", linewidth=2)
    path_axis.plot(0, 0, marker="o", color="#111827")
    path_axis.plot(RANGE, 0, marker="x", color="#dc2626", markersize=10, mew=3)
    path_axis.text(-0.6, -1.2, "O")
    path_axis.text(RANGE - 0.5, -1.2, "P")
    for x_values, y_values in trajectories.values():
        path_axis.plot(x_values, y_values, color="#cbd5e1", linewidth=1, linestyle="--")
    path_axis.set_xlim(-1, RANGE + 2)
    path_axis.set_ylim(-2, max_height + 3)
    path_axis.set_title("Trajectories that all reach P")
    path_axis.set_xlabel("horizontal distance x [m]")
    path_axis.set_ylabel("height y [m]")
    path_axis.grid(alpha=0.2)
    current_path, = path_axis.plot([], [], color="#2563eb", linewidth=2.8)
    path_info = path_axis.text(
        0.03,
        0.96,
        "",
        transform=path_axis.transAxes,
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    curve_angles = list(range(1, 90))
    curve_speeds = [initial_speed(angle) for angle in curve_angles]
    speed_axis.plot(curve_angles, curve_speeds, color="#64748b", linewidth=2)
    speed_axis.axvline(45, color="#9ca3af", linestyle="--")
    speed_axis.axhline(min_speed, color="#9ca3af", linestyle="--")
    speed_axis.text(46, min_speed + 0.35, "minimum at 45 deg", color="#475569")
    speed_axis.set_xlim(0, 90)
    speed_axis.set_ylim(min_speed - 1, max(curve_speeds) * 1.05)
    speed_axis.set_title("Required initial speed")
    speed_axis.set_xlabel("launch angle theta [deg]")
    speed_axis.set_ylabel("initial speed v0 [m/s]")
    speed_axis.grid(alpha=0.2)
    current_point, = speed_axis.plot([], [], marker="o", color="#dc2626", markersize=8)
    speed_info = speed_axis.text(
        0.03,
        0.96,
        "",
        transform=speed_axis.transAxes,
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        angle = ANGLES[frame]
        speed = speeds[frame]
        x_values, y_values = trajectories[angle]
        current_path.set_data(x_values, y_values)
        current_point.set_data([angle], [speed])
        path_info.set_text(
            f"theta = {angle} deg\n"
            f"v0 = sqrt(gL / sin(2 theta))\n"
            f"   = {speed:.2f} m/s"
        )
        speed_info.set_text(
            f"sin(2 theta) = {sin(2 * radians(angle)):.3f}\n"
            f"minimum speed = sqrt(gL) = {min_speed:.2f} m/s"
        )
        return current_path, path_info, current_point, speed_info

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(len(ANGLES)),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._projectile_range_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
