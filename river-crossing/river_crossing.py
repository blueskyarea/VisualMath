"""川を横切る船の相対速度と航跡を可視化する。"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


RIVER_WIDTH = 20.0
CURRENT = (1.5, 0.0)  # x 軸を下流、y 軸を対岸方向とする。
CASES = (
    {
        "title": "(1) Bow points straight across",
        "boat_water": (0.0, 2.0),
        "ground": (1.5, 2.0),
        "speed": "shore speed = 2.5 m/s",
        "time": "crossing time = 10 s",
    },
    {
        "title": "(2) Bow points upstream",
        "boat_water": (-1.5, 2.0),
        "ground": (0.0, 2.0),
        "speed": "shore speed = 2.0 m/s",
        "time": "crossing time = 10 s",
    },
)


def make_arrow(axis, color):
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


def set_arrow(arrow, start, vector):
    arrow.set_positions(start, (start[0] + vector[0], start[1] + vector[1]))


def setup_axis(axis, case):
    axis.axhspan(0, RIVER_WIDTH, color="#dbeafe")
    axis.axhline(0, color="#334155", linewidth=3)
    axis.axhline(RIVER_WIDTH, color="#334155", linewidth=3)
    axis.text(-7.5, -0.9, "starting bank", fontsize=10)
    axis.text(-7.5, RIVER_WIDTH + 0.5, "opposite bank", fontsize=10)
    axis.text(15.5, 1.0, "downstream ->", color="#0369a1", fontsize=10)
    axis.set_title(case["title"])
    axis.set_xlim(-9, 22)
    axis.set_ylim(-1.5, 23.5)
    axis.set_aspect("equal")
    axis.set_xlabel("downstream (+) / upstream (-) [m]")
    axis.set_ylabel("across the river [m]")
    axis.set_yticks((0, 10, 20))
    axis.grid(alpha=0.2)

    # 矢印は「対水速度 + 流速 = 岸から見た速度」を表す。
    water_arrow = make_arrow(axis, "#2563eb")
    current_arrow = make_arrow(axis, "#16a34a")
    ground_arrow = make_arrow(axis, "#dc2626")
    boat, = axis.plot([], [], marker="o", color="#111827", markersize=8)
    trail, = axis.plot([], [], color="#7c3aed", linewidth=1.8, linestyle="--")
    info = axis.text(
        0.03,
        0.97,
        "",
        transform=axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )
    legend = axis.text(
        0.03,
        0.07,
        "blue: boat relative to water\ngreen: current\nred: boat relative to shore",
        transform=axis.transAxes,
        va="bottom",
        fontsize=8.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )
    return water_arrow, current_arrow, ground_arrow, boat, trail, info, legend


def main(interval_ms=100):
    figure, axes = plt.subplots(1, 2, figsize=(14, 8))
    figure.suptitle("River crossing: boat velocity + current = velocity seen from shore")
    artists = [setup_axis(axis, case) for axis, case in zip(axes, CASES)]

    def update(frame):
        time = frame / 10  # 0.0 s から 10.0 s までを 0.1 s ごとに表示する。
        changed = []
        for case, item in zip(CASES, artists):
            water_arrow, current_arrow, ground_arrow, boat, trail, info, legend = item
            ground_x, ground_y = case["ground"]
            position = (ground_x * time, ground_y * time)
            set_arrow(water_arrow, position, case["boat_water"])
            set_arrow(current_arrow, position, CURRENT)
            set_arrow(ground_arrow, position, case["ground"])
            boat.set_data([position[0]], [position[1]])
            trail.set_data([0, position[0]], [0, position[1]])
            info.set_text(
                f"t = {time:.1f} s\n"
                f"{case['speed']}\n{case['time']}"
            )
            changed.extend((water_arrow, current_arrow, ground_arrow, boat, trail, info, legend))
        return changed

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
    figure._river_crossing_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
