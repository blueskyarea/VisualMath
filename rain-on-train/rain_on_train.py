"""走行する電車内で見える雨の相対速度を可視化する。"""

from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Arc, FancyArrowPatch


TRAIN_SPEED = 4.0
RAIN_SPEED = 4.0 * sqrt(3)


def add_arrow(axis, color):
    arrow = FancyArrowPatch(
        (0, 0),
        (0, 0),
        arrowstyle="->",
        mutation_scale=16,
        linewidth=2.6,
        color=color,
    )
    axis.add_patch(arrow)
    return arrow


def set_arrow(arrow, vector):
    arrow.set_positions((0, 0), vector)


def setup_axis(axis, title):
    axis.axhline(0, color="#9ca3af", linewidth=1)
    axis.axvline(0, color="#9ca3af", linewidth=1)
    axis.set_xlim(-8, 8)
    axis.set_ylim(-9, 3)
    axis.set_aspect("equal")
    axis.set_title(title)
    axis.set_xlabel("east (+) / west (-)  [m/s]")
    axis.set_ylabel("up (+) / down (-)  [m/s]")
    axis.grid(alpha=0.2)


def main(interval_ms=1200):
    figure, (ground_axis, train_axis) = plt.subplots(1, 2, figsize=(13, 6))
    figure.suptitle("Rain seen from a moving train")
    setup_axis(ground_axis, "Ground reference frame")
    setup_axis(train_axis, "Passenger reference frame")

    rain_ground = add_arrow(ground_axis, "#2563eb")
    train_ground = add_arrow(ground_axis, "#dc2626")
    rain_seen = add_arrow(train_axis, "#16a34a")
    vertical_component, = train_axis.plot(
        [0, 0], [0, -RAIN_SPEED], color="#6b7280", linestyle="--"
    )
    horizontal_component, = train_axis.plot(
        [0, -TRAIN_SPEED], [-RAIN_SPEED, -RAIN_SPEED], color="#6b7280", linestyle="--"
    )
    angle = Arc((0, 0), 3.0, 3.0, theta1=240, theta2=270, color="#111827", linewidth=1.5)
    train_axis.add_patch(angle)

    ground_info = ground_axis.text(
        0.03,
        0.96,
        "",
        transform=ground_axis.transAxes,
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )
    train_info = train_axis.text(
        0.03,
        0.96,
        "",
        transform=train_axis.transAxes,
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )
    answer = train_axis.text(
        0.03,
        0.06,
        "",
        transform=train_axis.transAxes,
        va="bottom",
        fontsize=10,
        bbox={"facecolor": "#fef3c7", "edgecolor": "none", "alpha": 0.95},
    )

    def update(frame):
        # 地面の雨、電車、電車内で見える雨の順で表示する。
        show_rain = frame >= 1
        show_train = frame >= 2
        show_relative = frame >= 3

        set_arrow(rain_ground, (0, -RAIN_SPEED))
        set_arrow(train_ground, (TRAIN_SPEED, 0))
        set_arrow(rain_seen, (-TRAIN_SPEED, -RAIN_SPEED))
        rain_ground.set_visible(show_rain)
        train_ground.set_visible(show_train)
        rain_seen.set_visible(show_relative)
        vertical_component.set_visible(show_relative)
        horizontal_component.set_visible(show_relative)
        angle.set_visible(show_relative)

        ground_info.set_text(
            "rain: 4sqrt(3) m/s downward" if show_rain else ""
        )
        if show_train:
            ground_info.set_text(
                "rain: 4sqrt(3) m/s downward\ntrain: 4.0 m/s east"
            )
        train_info.set_text(
            "v_rain/train = v_rain/ground - v_train/ground\n"
            "= (-4, -4sqrt(3)) m/s"
            if show_relative
            else ""
        )
        answer.set_text(
            "tan 30 deg = 4 / v\nv = 4sqrt(3) m/s = 6.92 m/s"
            if show_relative
            else ""
        )
        return (
            rain_ground,
            train_ground,
            rain_seen,
            vertical_component,
            horizontal_component,
            angle,
            ground_info,
            train_info,
            answer,
        )

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(4),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._rain_on_train_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
