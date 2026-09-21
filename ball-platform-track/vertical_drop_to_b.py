"""台上の鉛直部分 A-B を小球が落下する様子を可視化する。"""

from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


GRAVITY = 9.8
H1 = 4.0
H2 = 2.0
HORIZONTAL_LENGTH = 3.5
CURVE_WIDTH = 2.2
FALL_TIME = sqrt(2 * (H1 - H2) / GRAVITY)
SPEED_AT_B = sqrt(2 * GRAVITY * (H1 - H2))
VECTOR_SCALE = 0.12


def make_curve():
    """B で鉛直、C で水平につながる3次ベジェ曲線を作る。"""
    points = []
    for index in range(101):
        u = index / 100
        # B=(0,H2), control1=(0,H2/2), control2=(CURVE_WIDTH*0.65,0), C=(CURVE_WIDTH,0)
        x = 3 * (1 - u) * u**2 * CURVE_WIDTH * 0.65 + u**3 * CURVE_WIDTH
        y = (1 - u) ** 3 * H2 + 3 * (1 - u) ** 2 * u * (H2 / 2)
        points.append((x, y))
    return points


def main(interval_ms=70):
    curve = make_curve()
    figure, axis = plt.subplots(figsize=(10, 6))
    figure.suptitle("Ball falling from A to B on a platform")

    # 台に固定された軌道 A-B-C-D と、D の鉛直な壁を描く。
    axis.plot((0, 0), (0, H1), color="#475569", linewidth=5)
    axis.plot([point[0] for point in curve], [point[1] for point in curve], color="#475569", linewidth=5)
    axis.plot((CURVE_WIDTH, CURVE_WIDTH + HORIZONTAL_LENGTH), (0, 0), color="#475569", linewidth=5)
    axis.plot(
        (CURVE_WIDTH + HORIZONTAL_LENGTH, CURVE_WIDTH + HORIZONTAL_LENGTH),
        (0, 1.4),
        color="#7c2d12",
        linewidth=5,
    )
    axis.axhline(-0.45, color="#334155", linewidth=3)
    axis.text(2.2, -0.8, "smooth horizontal floor", color="#334155")
    axis.text(-0.28, H1 + 0.15, "A")
    axis.text(-0.28, H2 + 0.10, "B")
    axis.text(CURVE_WIDTH - 0.05, 0.18, "C")
    axis.text(CURVE_WIDTH + HORIZONTAL_LENGTH - 0.05, 0.18, "D")
    axis.annotate("h1", xy=(-0.75, H1), xytext=(-0.75, 0), arrowprops={"arrowstyle": "<->"}, ha="center")
    axis.annotate("h2", xy=(-1.20, H2), xytext=(-1.20, 0), arrowprops={"arrowstyle": "<->"}, ha="center")
    axis.set_xlim(-1.8, CURVE_WIDTH + HORIZONTAL_LENGTH + 1.2)
    axis.set_ylim(-1.1, H1 + 1.0)
    axis.set_aspect("equal")
    axis.set_title("(1) Vertical fall from A to B")
    axis.set_xlabel("horizontal direction")
    axis.set_ylabel("vertical direction")
    axis.set_xticks([])
    axis.set_yticks([])
    axis.grid(alpha=0.15)

    ball, = axis.plot([], [], marker="o", color="#2563eb", markersize=10)
    velocity_arrow = FancyArrowPatch(
        (0, 0),
        (0, 0),
        arrowstyle="->",
        mutation_scale=14,
        linewidth=2.2,
        color="#dc2626",
    )
    axis.add_patch(velocity_arrow)
    info = axis.text(
        0.03,
        0.95,
        "",
        transform=axis.transAxes,
        va="top",
        fontsize=9.5,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = FALL_TIME * frame / 100
        height = H1 - GRAVITY * time**2 / 2
        vertical_speed = -GRAVITY * time
        ball.set_data([0], [height])
        velocity_arrow.set_positions(
            (0, height),
            (0, height + vertical_speed * VECTOR_SCALE),
        )
        info.set_text(
            f"t = {time:.2f} / {FALL_TIME:.2f} s\n"
            "platform horizontal speed = 0\n"
            f"vertical speed = {vertical_speed:.2f}\n"
            f"at B: vB = sqrt(2g(h1-h2)) = {SPEED_AT_B:.2f}"
        )
        return ball, velocity_arrow, info

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
    figure._vertical_drop_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
