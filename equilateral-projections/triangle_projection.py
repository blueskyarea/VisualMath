"""正三角形で繰り返す垂線投影を可視化するプログラム。"""

from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


SIDE = 3.0
HEIGHT = SIDE * sqrt(3) / 2
A = (0.0, 0.0)
B = (SIDE, 0.0)
C = (SIDE / 2, HEIGHT)


def project_to_line(point, start, end):
    """point の、start--end を含む直線への正射影を返す。"""
    vx, vy = end[0] - start[0], end[1] - start[1]
    wx, wy = point[0] - start[0], point[1] - start[1]
    scale = (wx * vx + wy * vy) / (vx * vx + vy * vy)
    return (start[0] + scale * vx, start[1] + scale * vy)


def make_step(p):
    """P から Q, R を経由して次の P を作る。"""
    q = project_to_line(p, B, C)
    r = project_to_line(q, C, A)
    next_p = project_to_line(r, A, B)
    return q, r, next_p


def build_points(count):
    """P1 から P_count までと、各投影点を生成する。"""
    points = [(2.0, 0.0)]  # AP1 = 2
    steps = []
    for _ in range(count - 1):
        q, r, next_p = make_step(points[-1])
        steps.append((points[-1], q, r, next_p))
        points.append(next_p)
    return points, steps


def main(count=10, interval_ms=1000):
    points, steps = build_points(count)
    lengths = [p[0] for p in points]

    figure, (ax_geometry, ax_sequence) = plt.subplots(1, 2, figsize=(12, 5))
    figure.suptitle("Repeated perpendicular projections in an equilateral triangle")

    ax_geometry.plot(
        [A[0], B[0], C[0], A[0]],
        [A[1], B[1], C[1], A[1]],
        color="#1f2937",
        linewidth=2,
    )
    for name, point in (("A", A), ("B", B), ("C", C)):
        ax_geometry.annotate(name, point, xytext=(6, 6), textcoords="offset points")
    ax_geometry.set_aspect("equal")
    ax_geometry.set_xlim(-0.35, 3.35)
    ax_geometry.set_ylim(-0.35, HEIGHT + 0.35)
    ax_geometry.set_title("Geometry")
    ax_geometry.axis("off")

    ax_sequence.axhline(1, color="#9ca3af", linestyle="--", label="limit = 1")
    ax_sequence.set_xlim(0.7, count + 0.3)
    ax_sequence.set_ylim(min(lengths + [1]) - 0.2, max(lengths + [1]) + 0.2)
    ax_sequence.set_xticks(range(1, count + 1))
    ax_sequence.set_xlabel("n")
    ax_sequence.set_ylabel("AP_n")
    ax_sequence.set_title("Length sequence")
    ax_sequence.grid(alpha=0.25)
    ax_sequence.legend()

    path_line, = ax_geometry.plot([], [], color="#ef4444", linewidth=1.8, marker="o")
    sequence_line, = ax_sequence.plot([], [], color="#2563eb", marker="o")
    info = ax_geometry.text(
        0.02,
        0.98,
        "",
        transform=ax_geometry.transAxes,
        va="top",
        bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
    )

    def init():
        """GTK3Agg で最初のフレームを確実に空の状態から描画する。"""
        path_line.set_data([], [])
        sequence_line.set_data([], [])
        info.set_text("")
        return path_line, sequence_line, info

    def update(frame):
        # frame 0 は P1 のみ、以降は P -> Q -> R -> 次の P を表示する。
        completed = min(frame, len(steps))
        visible = [points[0]]
        for p, q, r, next_p in steps[:completed]:
            visible.extend((q, r, next_p))
        path_line.set_data([p[0] for p in visible], [p[1] for p in visible])

        current_n = completed + 1
        sequence_line.set_data(range(1, current_n + 1), lengths[:current_n])
        formula_value = 1 + (-1 / 8) ** (current_n - 1)
        info.set_text(
            f"P{current_n}: AP{current_n} = {lengths[current_n - 1]:.8f}\n"
            f"1 + (-1/8)^({current_n - 1}) = {formula_value:.8f}"
        )
        return path_line, sequence_line, info

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=len(steps) + 1,
        interval=interval_ms,
        blit=True,
        repeat=True,
        cache_frame_data=False,
    )
    # animation を参照し続けて、表示中にガベージコレクションされないようにする。
    figure._projection_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
