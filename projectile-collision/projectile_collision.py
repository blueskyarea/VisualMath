"""投射した小球と、同時に自由落下する小球の衝突を可視化する。"""

from math import atan2, cos, degrees, sin

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


GRAVITY = 9.8
X0 = 20.0
Y0 = 15.0
V0 = 20.0
THETA = atan2(Y0, X0)  # tan(theta) = y0 / x0 となる角度。
HIT_TIME = X0 / (V0 * cos(THETA))


def ball_1_position(time):
    return (
        V0 * cos(THETA) * time,
        V0 * sin(THETA) * time - GRAVITY * time**2 / 2,
    )


def ball_2_position(time):
    return X0, Y0 - GRAVITY * time**2 / 2


def main(interval_ms=80):
    times = [HIT_TIME * index / 100 for index in range(101)]
    ball_1_path = [ball_1_position(time) for time in times]
    ball_2_path = [ball_2_position(time) for time in times]
    hit_x, hit_y = ball_1_position(HIT_TIME)

    figure, (motion_axis, height_axis) = plt.subplots(1, 2, figsize=(14, 6))
    figure.suptitle("Projectile meets a falling ball")

    motion_axis.axhline(0, color="#334155", linewidth=2)
    motion_axis.axvline(0, color="#334155", linewidth=1)
    motion_axis.plot(X0, Y0, marker="o", markerfacecolor="none", color="#16a34a", markersize=10)
    motion_axis.text(X0 + 0.6, Y0 + 0.4, "P(x0, y0)", color="#16a34a")
    motion_axis.plot((0, X0), (0, Y0), color="#9ca3af", linestyle="--", linewidth=1.2)
    motion_axis.text(5, 5.0, "launch direction theta0", color="#475569")
    motion_axis.plot(
        [point[0] for point in ball_1_path],
        [point[1] for point in ball_1_path],
        color="#bfdbfe",
        linestyle="--",
    )
    motion_axis.plot(
        [point[0] for point in ball_2_path],
        [point[1] for point in ball_2_path],
        color="#bbf7d0",
        linestyle="--",
    )
    motion_axis.plot(hit_x, hit_y, marker="x", color="#dc2626", markersize=10, mew=3)
    motion_axis.text(hit_x + 0.5, hit_y - 1.0, "collision", color="#dc2626")
    motion_axis.set_xlim(-1, X0 + 5)
    motion_axis.set_ylim(-1, Y0 + 5)
    motion_axis.set_aspect("equal")
    motion_axis.set_title("Positions in the ground reference frame")
    motion_axis.set_xlabel("x")
    motion_axis.set_ylabel("y")
    motion_axis.grid(alpha=0.2)
    ball_1, = motion_axis.plot([], [], marker="o", color="#2563eb", markersize=9, label="ball 1")
    ball_2, = motion_axis.plot([], [], marker="o", color="#16a34a", markersize=9, label="ball 2")
    motion_axis.legend(loc="upper left")
    motion_info = motion_axis.text(
        0.03,
        0.96,
        "",
        transform=motion_axis.transAxes,
        va="top",
        fontsize=9.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    y_1_values = [position[1] for position in ball_1_path]
    y_2_values = [position[1] for position in ball_2_path]
    height_axis.plot(times, y_1_values, color="#2563eb", label="y1: ball 1")
    height_axis.plot(times, y_2_values, color="#16a34a", label="y2: ball 2")
    height_axis.axvline(HIT_TIME, color="#dc2626", linestyle="--")
    height_axis.set_title("Heights at the same time")
    height_axis.set_xlabel("time t [s]")
    height_axis.set_ylabel("height y")
    height_axis.grid(alpha=0.2)
    height_axis.legend()
    current_1, = height_axis.plot([], [], marker="o", color="#2563eb", markersize=7)
    current_2, = height_axis.plot([], [], marker="o", color="#16a34a", markersize=7)
    formula = height_axis.text(
        0.03,
        0.96,
        "",
        transform=height_axis.transAxes,
        va="top",
        fontsize=9.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = times[frame]
        x_1, y_1 = ball_1_position(time)
        x_2, y_2 = ball_2_position(time)
        ball_1.set_data([x_1], [y_1])
        ball_2.set_data([x_2], [y_2])
        current_1.set_data([time], [y_1])
        current_2.set_data([time], [y_2])
        motion_info.set_text(
            f"theta0 = {degrees(THETA):.2f} deg\n"
            f"t = {time:.2f} s\n"
            f"both fall by {GRAVITY * time**2 / 2:.2f}"
        )
        formula.set_text(
            "tan(theta0) = y0 / x0\n"
            f"collision time = {HIT_TIME:.2f} s\n"
            f"y1 = y2 = {y_1:.2f} at collision" if frame == 100 else
            "tan(theta0) = y0 / x0\n"
            f"collision time = {HIT_TIME:.2f} s"
        )
        return ball_1, ball_2, current_1, current_2, motion_info, formula

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(101),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._projectile_collision_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
