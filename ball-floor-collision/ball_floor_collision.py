"""なめらかな床で跳ね返るボールの速度成分と反発係数を可視化する。"""

from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


HORIZONTAL_SPEED = 1.0
INCOMING_VERTICAL_SPEED = sqrt(3)
OUTGOING_VERTICAL_SPEED = 1 / sqrt(3)
REST_COEFFICIENT = 1 / 3
COLLISION_TIME = 1.0
VECTOR_SCALE = 0.35


def add_arrow(axis, color):
    arrow = FancyArrowPatch(
        (0, 0),
        (0, 0),
        arrowstyle="->",
        mutation_scale=15,
        linewidth=2.4,
        color=color,
    )
    axis.add_patch(arrow)
    return arrow


def set_arrow(arrow, start, vector):
    arrow.set_positions(start, (start[0] + vector[0], start[1] + vector[1]))


def main(interval_ms=60):
    figure, (motion_axis, vector_axis) = plt.subplots(1, 2, figsize=(13, 6))
    figure.suptitle("Elastic collision with a smooth floor")

    # 左: 実際の運動
    motion_axis.axhline(0, color="#334155", linewidth=3)
    motion_axis.text(-2.5, -0.45, "smooth floor", color="#334155")
    motion_axis.plot((-1, 0), (INCOMING_VERTICAL_SPEED, 0), color="#bfdbfe", linestyle="--")
    motion_axis.plot((0, 1), (0, OUTGOING_VERTICAL_SPEED), color="#fecaca", linestyle="--")
    motion_axis.set_xlim(-1.6, 1.6)
    motion_axis.set_ylim(-0.7, 2.4)
    motion_axis.set_aspect("equal")
    motion_axis.set_title("Motion before and after collision")
    motion_axis.set_xlabel("horizontal direction")
    motion_axis.set_ylabel("vertical direction")
    motion_axis.grid(alpha=0.2)
    ball, = motion_axis.plot([], [], marker="o", color="#111827", markersize=10)
    incoming_arrow = add_arrow(motion_axis, "#2563eb")
    outgoing_arrow = add_arrow(motion_axis, "#dc2626")
    motion_info = motion_axis.text(
        0.03,
        0.96,
        "",
        transform=motion_axis.transAxes,
        va="top",
        fontsize=9.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # 右: 速度ベクトルの成分
    vector_axis.axhline(0, color="#9ca3af", linewidth=1)
    vector_axis.axvline(0, color="#9ca3af", linewidth=1)
    vector_axis.annotate(
        "",
        xy=(HORIZONTAL_SPEED, -INCOMING_VERTICAL_SPEED),
        xytext=(0, 0),
        arrowprops={"arrowstyle": "->", "color": "#2563eb", "lw": 2.6},
    )
    vector_axis.annotate(
        "",
        xy=(HORIZONTAL_SPEED, OUTGOING_VERTICAL_SPEED),
        xytext=(0, 0),
        arrowprops={"arrowstyle": "->", "color": "#dc2626", "lw": 2.6},
    )
    vector_axis.plot((HORIZONTAL_SPEED, HORIZONTAL_SPEED), (-INCOMING_VERTICAL_SPEED, OUTGOING_VERTICAL_SPEED), color="#94a3b8", linestyle="--")
    vector_axis.text(HORIZONTAL_SPEED + 0.1, -INCOMING_VERTICAL_SPEED / 2, "incoming\nvy = -sqrt(3)", color="#2563eb")
    vector_axis.text(HORIZONTAL_SPEED + 0.1, OUTGOING_VERTICAL_SPEED / 2, "outgoing\nvy = 1/sqrt(3)", color="#dc2626")
    vector_axis.text(HORIZONTAL_SPEED / 2, -0.35, "vx = 1 (unchanged)", ha="center")
    vector_axis.set_xlim(-0.6, 2.7)
    vector_axis.set_ylim(-2.3, 1.4)
    vector_axis.set_aspect("equal")
    vector_axis.set_title("Velocity components")
    vector_axis.set_xlabel("horizontal velocity vx")
    vector_axis.set_ylabel("vertical velocity vy")
    vector_axis.grid(alpha=0.2)
    vector_axis.text(
        0.03,
        0.95,
        "No friction: vx is unchanged\n"
        "e = outgoing vertical speed / incoming vertical speed\n"
        "  = (1/sqrt(3)) / sqrt(3) = 1/3",
        transform=vector_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = 2 * frame / 100
        if time <= COLLISION_TIME:
            # 入射速度は (1, -sqrt(3))。
            position = (time - 1, INCOMING_VERTICAL_SPEED * (1 - time))
            ball.set_data([position[0]], [position[1]])
            set_arrow(
                incoming_arrow,
                position,
                (HORIZONTAL_SPEED * VECTOR_SCALE, -INCOMING_VERTICAL_SPEED * VECTOR_SCALE),
            )
            incoming_arrow.set_visible(True)
            outgoing_arrow.set_visible(False)
            motion_info.set_text(
                "before collision\n"
                "speed = 2.0 m/s\n"
                "angle with floor = 60 deg\n"
                "(vx, vy) = (1, -sqrt(3))"
            )
        else:
            # 反射後の速度は (1, 1/sqrt(3))。
            after_time = time - COLLISION_TIME
            position = (after_time, OUTGOING_VERTICAL_SPEED * after_time)
            ball.set_data([position[0]], [position[1]])
            set_arrow(
                outgoing_arrow,
                position,
                (HORIZONTAL_SPEED * VECTOR_SCALE, OUTGOING_VERTICAL_SPEED * VECTOR_SCALE),
            )
            incoming_arrow.set_visible(False)
            outgoing_arrow.set_visible(True)
            motion_info.set_text(
                "after collision\n"
                "angle with floor = 30 deg\n"
                "(vx, vy) = (1, 1/sqrt(3))\n"
                "coefficient of restitution e = 1/3"
            )
        return ball, incoming_arrow, outgoing_arrow, motion_info

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
    figure._ball_floor_collision_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
