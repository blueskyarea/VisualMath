"""正面衝突する2物体の相対速度と反発係数を可視化する。"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


SPEED_A_BEFORE = 4.0
SPEED_B_BEFORE = 1.6
SPEED_A_AFTER = 1.5
SPEED_B_AFTER = 1.3
APPROACH_SPEED = SPEED_A_BEFORE + SPEED_B_BEFORE
SEPARATION_SPEED = SPEED_A_AFTER + SPEED_B_AFTER
REST_COEFFICIENT = SEPARATION_SPEED / APPROACH_SPEED
VECTOR_SCALE = 0.35


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


def set_arrow(arrow, start, velocity):
    arrow.set_positions(start, (start[0] + velocity * VECTOR_SCALE, start[1]))


def main(interval_ms=60):
    figure, (motion_axis, graph_axis) = plt.subplots(1, 2, figsize=(13, 6))
    figure.suptitle("Head-on collision and coefficient of restitution")

    # 左: 直線上での運動
    motion_axis.axhline(0, color="#334155", linewidth=2)
    motion_axis.axvline(0, color="#9ca3af", linestyle="--")
    motion_axis.text(-0.45, -0.65, "collision point")
    motion_axis.set_xlim(-4.8, 2.5)
    motion_axis.set_ylim(-1.0, 1.2)
    motion_axis.set_aspect("equal")
    motion_axis.set_title("Motion on a straight line")
    motion_axis.set_xlabel("position")
    motion_axis.set_yticks([])
    motion_axis.grid(alpha=0.2)
    object_a, = motion_axis.plot([], [], marker="o", color="#2563eb", markersize=12, label="A")
    object_b, = motion_axis.plot([], [], marker="o", color="#dc2626", markersize=12, label="B")
    arrow_a = add_arrow(motion_axis, "#2563eb")
    arrow_b = add_arrow(motion_axis, "#dc2626")
    motion_axis.legend(loc="upper right")
    motion_info = motion_axis.text(
        0.03,
        0.95,
        "",
        transform=motion_axis.transAxes,
        va="top",
        fontsize=9.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # 右: 位置と時刻の関係。傾きが速度を表す。
    pre_times = [-1 + index / 100 for index in range(101)]
    post_times = [index / 100 for index in range(101)]
    graph_axis.plot(pre_times, [SPEED_A_BEFORE * time for time in pre_times], color="#2563eb")
    graph_axis.plot(post_times, [-SPEED_A_AFTER * time for time in post_times], color="#2563eb", linestyle="--")
    graph_axis.plot(pre_times, [-SPEED_B_BEFORE * time for time in pre_times], color="#dc2626")
    graph_axis.plot(post_times, [SPEED_B_AFTER * time for time in post_times], color="#dc2626", linestyle="--")
    graph_axis.axvline(0, color="#334155", linewidth=1.5)
    graph_axis.set_title("Position-time graph")
    graph_axis.set_xlabel("time (collision at t = 0)")
    graph_axis.set_ylabel("position")
    graph_axis.grid(alpha=0.2)
    graph_axis.text(-0.95, -4.2, "solid: before collision\ndashed: after collision", fontsize=8.5)
    graph_axis.text(
        0.03,
        0.95,
        "approach speed = 4.0 + 1.6 = 5.6 m/s\n"
        "separation speed = 1.5 + 1.3 = 2.8 m/s\n"
        "e = 2.8 / 5.6 = 0.50",
        transform=graph_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )
    point_a, = graph_axis.plot([], [], marker="o", color="#2563eb", markersize=7)
    point_b, = graph_axis.plot([], [], marker="o", color="#dc2626", markersize=7)

    def update(frame):
        time = -1 + 2 * frame / 120
        if time < 0:
            position_a = SPEED_A_BEFORE * time
            position_b = -SPEED_B_BEFORE * time
            velocity_a = SPEED_A_BEFORE
            velocity_b = -SPEED_B_BEFORE
            motion_info.set_text(
                "before collision\n"
                "A: 4.0 m/s to the right\n"
                "B: 1.6 m/s to the left\n"
                f"approach speed = {APPROACH_SPEED:.1f} m/s"
            )
        else:
            position_a = -SPEED_A_AFTER * time
            position_b = SPEED_B_AFTER * time
            velocity_a = -SPEED_A_AFTER
            velocity_b = SPEED_B_AFTER
            motion_info.set_text(
                "after collision\n"
                "A: 1.5 m/s to the left\n"
                "B: 1.3 m/s to the right\n"
                f"separation speed = {SEPARATION_SPEED:.1f} m/s"
            )

        object_a.set_data([position_a], [0])
        object_b.set_data([position_b], [0])
        set_arrow(arrow_a, (position_a, 0), velocity_a)
        set_arrow(arrow_b, (position_b, 0), velocity_b)
        point_a.set_data([time], [position_a])
        point_b.set_data([time], [position_b])
        return object_a, object_b, arrow_a, arrow_b, motion_info, point_a, point_b

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(121),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._head_on_collision_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
