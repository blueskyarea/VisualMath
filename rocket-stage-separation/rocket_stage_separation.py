"""宇宙船とエンジン分離を、2つの基準系で可視化する。"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


SHIP_SPEED = 10.0
RELATIVE_SPEED = 3.0
ENGINE_SPEED = SHIP_SPEED - RELATIVE_SPEED
VECTOR_SCALE = 0.22


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


def setup_axis(axis, title):
    axis.set_facecolor("#0f172a")
    axis.set_ylim(-1.5, 1.5)
    axis.set_yticks([])
    axis.set_title(title)
    axis.set_xlabel("forward direction")
    for spine in axis.spines.values():
        spine.set_color("#94a3b8")
    axis.tick_params(colors="#475569")


def main(interval_ms=60):
    figure, (ground_axis, ship_axis) = plt.subplots(1, 2, figsize=(13, 5))
    figure.suptitle("Engine separation: ground frame and spacecraft frame")
    setup_axis(ground_axis, "External reference frame")
    setup_axis(ship_axis, "Reference frame of spacecraft S")
    ground_axis.set_xlim(-2, 24)
    ship_axis.set_xlim(-8, 4)

    ship_ground, = ground_axis.plot([], [], marker=">", color="#60a5fa", markersize=13, label="spacecraft S")
    engine_ground, = ground_axis.plot([], [], marker="s", color="#f59e0b", markersize=10, label="engine E")
    ship_arrow = add_arrow(ground_axis, "#60a5fa")
    engine_arrow = add_arrow(ground_axis, "#f59e0b")
    ground_axis.legend(loc="upper left", facecolor="#e2e8f0")
    ground_info = ground_axis.text(
        0.03,
        0.92,
        "",
        transform=ground_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    ship_fixed, = ship_axis.plot(0, 0, marker=">", color="#60a5fa", markersize=13, label="spacecraft S")
    engine_relative, = ship_axis.plot([], [], marker="s", color="#f59e0b", markersize=10, label="engine E")
    relative_arrow = add_arrow(ship_axis, "#f59e0b")
    ship_axis.axvline(0, color="#94a3b8", linestyle="--")
    ship_info = ship_axis.text(
        0.03,
        0.92,
        "",
        transform=ship_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = 2 * frame / 100
        ship_position = SHIP_SPEED * time
        engine_position = ENGINE_SPEED * time
        relative_position = engine_position - ship_position

        ship_ground.set_data([ship_position], [0])
        engine_ground.set_data([engine_position], [0])
        set_arrow(ship_arrow, (ship_position, 0), SHIP_SPEED)
        set_arrow(engine_arrow, (engine_position, 0), ENGINE_SPEED)
        engine_relative.set_data([relative_position], [0])
        set_arrow(relative_arrow, (relative_position, 0), -RELATIVE_SPEED)
        ground_info.set_text(
            f"spacecraft: vs = {SHIP_SPEED:.1f}\n"
            f"engine: vE = vs - mu = {ENGINE_SPEED:.1f}\n"
            "both move forward"
        )
        ship_info.set_text(
            f"engine moves backward at mu = {RELATIVE_SPEED:.1f}\n"
            "vE - vs = -mu\n"
            "vE = vs - mu"
        )
        return (
            ship_ground,
            engine_ground,
            ship_arrow,
            engine_arrow,
            ground_info,
            engine_relative,
            relative_arrow,
            ship_info,
            ship_fixed,
        )

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
    figure._rocket_stage_separation_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
