"""45度で跳んで塀を越える車の、3つの設問を可視化する。"""

from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


GRAVITY = 9.8
WALL_HEIGHT = 5.0
MAX_ACCELERATION = 2.0
LAUNCH_SPEED = 2 * sqrt(GRAVITY * WALL_HEIGHT)
RUNUP_DISTANCE = 2 * GRAVITY * WALL_HEIGHT / MAX_ACCELERATION
VERTICAL_SPEED = LAUNCH_SPEED / sqrt(2)
HORIZONTAL_SPEED = VERTICAL_SPEED
APEX_TIME = sqrt(2 * WALL_HEIGHT / GRAVITY)
WALL_DISTANCE = HORIZONTAL_SPEED * APEX_TIME


def main(interval_ms=80):
    frame_count = 100
    flight_times = [APEX_TIME * index / frame_count for index in range(frame_count + 1)]
    flight_x = [HORIZONTAL_SPEED * time for time in flight_times]
    flight_y = [VERTICAL_SPEED * time - GRAVITY * time**2 / 2 for time in flight_times]

    figure, (flight_axis, velocity_axis, runup_axis) = plt.subplots(1, 3, figsize=(18, 6))
    figure.suptitle("Car jump over a wall: questions (1), (2), and (3)")

    # (1) 最高点までの空中運動
    flight_axis.axhline(0, color="#334155", linewidth=2)
    flight_axis.axvline(0, color="#64748b", linestyle="--")
    flight_axis.text(-0.9, -0.75, "jump ramp")
    flight_axis.plot((WALL_DISTANCE, WALL_DISTANCE), (0, WALL_HEIGHT), color="#7c2d12", linewidth=7)
    flight_axis.text(WALL_DISTANCE + 0.4, WALL_HEIGHT / 2, "wall\nh", color="#7c2d12", va="center")
    flight_axis.plot(flight_x, flight_y, color="#bfdbfe", linestyle="--")
    flight_axis.plot(WALL_DISTANCE, WALL_HEIGHT, marker="x", color="#dc2626", markersize=10, mew=3)
    flight_axis.set_xlim(-1.5, WALL_DISTANCE + 4)
    flight_axis.set_ylim(-1.5, WALL_HEIGHT + 2.5)
    flight_axis.set_aspect("equal")
    flight_axis.set_title("(1) Time to the wall top")
    flight_axis.set_xlabel("horizontal distance [m]")
    flight_axis.set_ylabel("height [m]")
    flight_axis.grid(alpha=0.2)
    car, = flight_axis.plot([], [], marker=">", color="#2563eb", markersize=12)
    air_trail, = flight_axis.plot([], [], color="#2563eb", linewidth=2.4)
    flight_info = flight_axis.text(
        0.03,
        0.96,
        "",
        transform=flight_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # (2) ジャンプ直後の速度ベクトル
    velocity_axis.axhline(0, color="#9ca3af", linewidth=1)
    velocity_axis.axvline(0, color="#9ca3af", linewidth=1)
    velocity_axis.annotate(
        "",
        xy=(HORIZONTAL_SPEED, VERTICAL_SPEED),
        xytext=(0, 0),
        arrowprops={"arrowstyle": "->", "color": "#2563eb", "lw": 2.8},
    )
    velocity_axis.plot((HORIZONTAL_SPEED, HORIZONTAL_SPEED), (0, VERTICAL_SPEED), color="#94a3b8", linestyle="--")
    velocity_axis.plot((0, HORIZONTAL_SPEED), (VERTICAL_SPEED, VERTICAL_SPEED), color="#94a3b8", linestyle="--")
    velocity_axis.text(HORIZONTAL_SPEED / 2, -1.3, "vx = sqrt(2gh)", ha="center")
    velocity_axis.text(HORIZONTAL_SPEED + 0.4, VERTICAL_SPEED / 2, "vy = sqrt(2gh)", va="center")
    velocity_axis.text(1.5, 0.5, "45 deg", color="#2563eb")
    velocity_axis.set_xlim(-1.5, HORIZONTAL_SPEED + 5)
    velocity_axis.set_ylim(-2.5, VERTICAL_SPEED + 4)
    velocity_axis.set_aspect("equal")
    velocity_axis.set_title("(2) Required speed at 45 deg")
    velocity_axis.set_xlabel("horizontal velocity component")
    velocity_axis.set_ylabel("vertical velocity component")
    velocity_axis.grid(alpha=0.2)
    velocity_axis.text(
        0.03,
        0.95,
        "v = 2sqrt(gh)\n"
        "vx = vy = v / sqrt(2)\n"
        "= sqrt(2gh)",
        transform=velocity_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # (3) 静止状態から最大加速度で加速するときの助走
    distances = [RUNUP_DISTANCE * index / frame_count for index in range(frame_count + 1)]
    runup_speeds = [sqrt(2 * MAX_ACCELERATION * distance) for distance in distances]
    runup_axis.plot(distances, runup_speeds, color="#64748b", linewidth=2)
    runup_axis.axvline(RUNUP_DISTANCE, color="#dc2626", linestyle="--")
    runup_axis.axhline(LAUNCH_SPEED, color="#dc2626", linestyle="--")
    runup_axis.set_xlim(0, RUNUP_DISTANCE * 1.1)
    runup_axis.set_ylim(0, LAUNCH_SPEED * 1.15)
    runup_axis.set_title("(3) Minimum run-up distance")
    runup_axis.set_xlabel("run-up distance [m]")
    runup_axis.set_ylabel("speed [m/s]")
    runup_axis.grid(alpha=0.2)
    runup_point, = runup_axis.plot([], [], marker="o", color="#dc2626", markersize=7)
    runup_info = runup_axis.text(
        0.03,
        0.95,
        "",
        transform=runup_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = flight_times[frame]
        x = flight_x[frame]
        y = flight_y[frame]
        car.set_data([x], [y])
        air_trail.set_data(flight_x[: frame + 1], flight_y[: frame + 1])
        flight_info.set_text(
            f"t = {time:.2f} / {APEX_TIME:.2f} s\n"
            f"height = {y:.2f} / {WALL_HEIGHT:.2f} m\n"
            "time to wall top = sqrt(2h/g)"
        )
        runup_point.set_data([distances[frame]], [runup_speeds[frame]])
        runup_info.set_text(
            f"v^2 = 2 alpha s\n"
            f"required v = 2sqrt(gh)\n"
            f"minimum s = 2gh/alpha\n"
            f"= {RUNUP_DISTANCE:.2f} m"
        )
        return car, air_trail, flight_info, runup_point, runup_info

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
    figure._car_jump_wall_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
