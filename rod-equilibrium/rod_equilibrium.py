"""一様な棒のつり合いを、力とモーメントで可視化する。"""

from math import cos, pi, sin

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


ROD_LENGTH = 0.80
ROD_WEIGHT = 40.0
FORCE_SCALE = 0.006  # 1 N を図中の 0.006 m として描く。


def add_force(axis, point, force, label, color):
    """point に作用する鉛直の力を表す矢印とラベルを作る。"""
    end = (point[0], point[1] + force * FORCE_SCALE)
    arrow = FancyArrowPatch(
        point,
        end,
        arrowstyle="->",
        mutation_scale=16,
        linewidth=2.4,
        color=color,
    )
    text = axis.text(
        end[0] + 0.025,
        end[1],
        label,
        color=color,
        fontsize=10,
        va="center",
    )
    axis.add_patch(arrow)
    return arrow, text


def make_case_1(axis):
    """両端を鉛直な糸でつった、30 度傾いた棒。"""
    angle = pi / 6
    left = (0.0, 0.0)
    right = (ROD_LENGTH * cos(angle), ROD_LENGTH * sin(angle))
    center = ((left[0] + right[0]) / 2, (left[1] + right[1]) / 2)
    axis.plot((left[0], right[0]), (left[1], right[1]), color="#374151", linewidth=7)
    axis.text(0.18, 0.08, "30 deg", fontsize=10)
    forces = (
        add_force(axis, center, -ROD_WEIGHT, "weight = 40 N", "#dc2626"),
        add_force(axis, left, 20, "T1 = 20 N", "#2563eb"),
        add_force(axis, right, 20, "T2 = 20 N", "#16a34a"),
    )
    result = "T1 + T2 = 40\nT2 (0.80 cos 30 deg) = 40 (0.40 cos 30 deg)\nT1 = T2 = 20 N"
    return forces, result


def make_case_2(axis):
    """左端と、左端から 0.60 m の位置で支持された水平な棒。"""
    left = (0.0, 0.0)
    center = (0.40, 0.0)
    second_support = (0.60, 0.0)
    axis.plot((0, ROD_LENGTH), (0, 0), color="#374151", linewidth=7)
    axis.plot((second_support[0], second_support[0]), (-0.04, 0.04), color="#6b7280")
    axis.text(0.48, -0.12, "0.60 m", fontsize=10)
    forces = (
        add_force(axis, center, -ROD_WEIGHT, "weight = 40 N", "#dc2626"),
        add_force(axis, left, 40 / 3, "T1 = 40/3 N", "#2563eb"),
        add_force(axis, second_support, 80 / 3, "T2 = 80/3 N", "#16a34a"),
    )
    result = "T1 + T2 = 40\nT2 x 0.60 = 40 x 0.40\nT1 = 40/3 N,  T2 = 80/3 N"
    return forces, result


def make_case_3(axis):
    """1 本の糸と右端の下向き 20 N でつり合う水平な棒。"""
    support_x = 8 / 15
    support = (support_x, 0.0)
    center = (0.40, 0.0)
    right = (ROD_LENGTH, 0.0)
    axis.plot((0, ROD_LENGTH), (0, 0), color="#374151", linewidth=7)
    axis.plot((support_x, support_x), (-0.04, 0.04), color="#6b7280")
    axis.text(support_x - 0.10, -0.12, "x = 8/15 m", fontsize=10)
    forces = (
        add_force(axis, center, -ROD_WEIGHT, "weight = 40 N", "#dc2626"),
        add_force(axis, support, 60, "T1 = 60 N", "#2563eb"),
        add_force(axis, right, -20, "20 N", "#16a34a"),
    )
    result = "T1 = 40 + 20 = 60 N\nT1 x x = 40 x 0.40 + 20 x 0.80\nx = 8/15 m = 0.533 m"
    return forces, result


def main(interval_ms=1200):
    figure, axes = plt.subplots(1, 3, figsize=(15, 5.5))
    figure.suptitle("Equilibrium of a uniform rod: forces and moments")
    builders = (make_case_1, make_case_2, make_case_3)
    titles = ("(1) Two end supports", "(2) Offset support", "(3) One support + 20 N")
    cases = []

    for axis, builder, title in zip(axes, builders, titles):
        forces, result = builder(axis)
        axis.set_title(title)
        axis.set_aspect("equal")
        axis.set_xlim(-0.12, 0.98)
        axis.set_ylim(-0.38, 0.58)
        axis.axis("off")
        result_text = axis.text(
            0.03,
            0.04,
            "",
            transform=axis.transAxes,
            va="bottom",
            fontsize=9,
            bbox={"facecolor": "#f3f4f6", "edgecolor": "none", "alpha": 0.95},
        )
        cases.append((forces, result, result_text))

    def update(frame):
        # 棒だけの状態から、重力、T1、最後の力の順に見せる。
        changed = []
        for forces, result, result_text in cases:
            for index, (arrow, label) in enumerate(forces):
                visible = index < frame
                arrow.set_visible(visible)
                label.set_visible(visible)
                changed.extend((arrow, label))
            result_text.set_text(result if frame >= 3 else "")
            changed.append(result_text)
        return changed

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
    figure._rod_equilibrium_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
