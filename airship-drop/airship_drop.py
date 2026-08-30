"""水平飛行する飛行船から落とした小球の運動を可視化する。"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


HEIGHT = 78.4
HORIZONTAL_SPEED = 20.0
GRAVITY = 9.8
FLIGHT_TIME = 4.0
TARGET_X = HORIZONTAL_SPEED * FLIGHT_TIME


def setup_ground_axis(axis):
    axis.axhline(0, color="#334155", linewidth=2)
    axis.plot(TARGET_X, 0, marker="x", color="#dc2626", markersize=11, mew=3)
    axis.text(TARGET_X - 6, -7, "target", color="#dc2626")
    axis.set_title("Ground reference frame")
    axis.set_xlim(-8, 90)
    axis.set_ylim(-8, 90)
    axis.set_aspect("equal")
    axis.set_xlabel("horizontal distance [m]")
    axis.set_ylabel("height [m]")
    axis.grid(alpha=0.2)
    airship, = axis.plot([], [], marker=">", color="#2563eb", markersize=12)
    ball, = axis.plot([], [], marker="o", color="#dc2626", markersize=7)
    trail, = axis.plot([], [], color="#dc2626", linestyle="--", linewidth=1.6)
    info = axis.text(
        0.03,
        0.96,
        "",
        transform=axis.transAxes,
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )
    return airship, ball, trail, info


def setup_airship_axis(axis):
    axis.axhline(0, color="#334155", linewidth=2)
    axis.axvline(0, color="#9ca3af", linewidth=1, linestyle="--")
    axis.plot(0, 0, marker=">", color="#2563eb", markersize=12)
    axis.text(1.2, 1.2, "airship", color="#2563eb")
    axis.set_title("Airship reference frame")
    axis.set_xlim(-12, 12)
    axis.set_ylim(-86, 8)
    axis.set_aspect("auto")
    axis.set_xlabel("horizontal distance relative to airship [m]")
    axis.set_ylabel("vertical distance relative to airship [m]")
    axis.grid(alpha=0.2)
    ball, = axis.plot([], [], marker="o", color="#dc2626", markersize=7)
    trail, = axis.plot([], [], color="#dc2626", linestyle="--", linewidth=1.6)
    info = axis.text(
        0.03,
        0.04,
        "",
        transform=axis.transAxes,
        va="bottom",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )
    return ball, trail, info


def main(interval_ms=80):
    figure, (ground_axis, airship_axis) = plt.subplots(1, 2, figsize=(14, 7))
    figure.suptitle("A ball dropped from a horizontally moving airship")
    ground_artists = setup_ground_axis(ground_axis)
    airship_artists = setup_airship_axis(airship_axis)

    def update(frame):
        time = frame / 20  # 0.00 s から 4.00 s までを 0.05 s ごとに描く。
        x = HORIZONTAL_SPEED * time
        y = HEIGHT - GRAVITY * time**2 / 2
        relative_y = -GRAVITY * time**2 / 2

        airship, ball_ground, trail_ground, ground_info = ground_artists
        ball_airship, trail_airship, airship_info = airship_artists
        airship.set_data([x], [HEIGHT])
        ball_ground.set_data([x], [y])
        trail_ground.set_data([HORIZONTAL_SPEED * step / 20 for step in range(frame + 1)], [
            HEIGHT - GRAVITY * (step / 20) ** 2 / 2 for step in range(frame + 1)
        ])
        ball_airship.set_data([0], [relative_y])
        trail_airship.set_data([0] * (frame + 1), [
            -GRAVITY * (step / 20) ** 2 / 2 for step in range(frame + 1)
        ])
        ground_info.set_text(
            f"t = {time:.2f} s\n"
            f"airship and ball: horizontal speed = {HORIZONTAL_SPEED:.1f} m/s\n"
            f"x = {x:.1f} m,  y = {y:.1f} m"
        )
        airship_info.set_text(
            f"t = {time:.2f} s\n"
            "horizontal relative speed = 0 m/s\n"
            f"vertical distance = {relative_y:.1f} m"
        )
        return (*ground_artists, *airship_artists)

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(81),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._airship_drop_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
