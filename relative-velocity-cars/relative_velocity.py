"""2台の自動車の相対速度を、速度ベクトルの三角形で表示する。"""

from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch


CAR_A_VELOCITY = (10.0, 0.0)  # 東を x 軸正方向、北を y 軸正方向とする。

CASES = (
    {
        "title": "Case 1: observer B",
        "observer": "v_B = 15 m/s west",
        "relative": "v_A/B = 25 m/s east",
        "answer": "B moves west at 15 m/s",
        "observer_velocity": (-15.0, 0.0),
        "relative_velocity": (25.0, 0.0),
    },
    {
        "title": "Case 2: observer C",
        "observer": "v_C = 10sqrt(3) m/s north",
        "relative": "v_A/C = 20 m/s, 60 deg south of east",
        "answer": "C moves north at 10sqrt(3) m/s = 17.3 m/s",
        "observer_velocity": (0.0, 10.0 * sqrt(3)),
        "relative_velocity": (10.0, -10.0 * sqrt(3)),
    },
)


def add_vector(axis, color):
    """開始点と終点を更新できる矢印とラベルを作る。"""
    arrow = FancyArrowPatch(
        (0, 0),
        (0, 0),
        arrowstyle="->",
        mutation_scale=18,
        linewidth=2.5,
        color=color,
    )
    label = axis.text(0, 0, "", color=color, fontsize=10, va="bottom")
    axis.add_patch(arrow)
    return arrow, label


def set_vector(arrow, label, start, vector, fraction, text):
    """ベクトルを fraction の長さまで描画する。"""
    end = (start[0] + vector[0] * fraction, start[1] + vector[1] * fraction)
    arrow.set_positions(start, end)
    label.set_position((end[0] + 0.4, end[1] + 0.4))
    label.set_text(text if fraction else "")


def setup_axis(axis, case):
    axis.axhline(0, color="#9ca3af", linewidth=1)
    axis.axvline(0, color="#9ca3af", linewidth=1)
    axis.set_aspect("equal")
    axis.set_xlim(-18, 13)
    axis.set_ylim(-20, 20)
    axis.set_xlabel("east (+) / west (-)  [m/s]")
    axis.set_ylabel("north (+) / south (-)  [m/s]")
    axis.set_title(case["title"])
    axis.grid(alpha=0.2)
    axis.text(
        0.03,
        0.96,
        "v_A = v_observer + v_A/observer",
        transform=axis.transAxes,
        va="top",
        fontsize=10,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85},
    )
    return {
        "observer": add_vector(axis, "#2563eb"),
        "relative": add_vector(axis, "#16a34a"),
        "a": add_vector(axis, "#dc2626"),
        "answer": axis.text(
            0.03,
            0.06,
            "",
            transform=axis.transAxes,
            va="bottom",
            fontsize=10,
            color="#111827",
            bbox={"facecolor": "#fef3c7", "edgecolor": "none", "alpha": 0.9},
        ),
    }


def main(interval_ms=1100):
    figure, axes = plt.subplots(1, 2, figsize=(13, 6))
    figure.suptitle("Relative velocity: v_A = v_observer + v_A/observer")
    artists = [setup_axis(axis, case) for axis, case in zip(axes, CASES)]

    def update(frame):
        # Aの速度、相対速度、観測者の速度の順で三角形を完成させる。
        a_fraction = min(frame, 1)
        relative_fraction = min(max(frame - 1, 0), 1)
        observer_fraction = min(max(frame - 2, 0), 1)
        changed = []

        for case, item in zip(CASES, artists):
            observer = case["observer_velocity"]
            relative = case["relative_velocity"]
            observer_arrow, observer_label = item["observer"]
            relative_arrow, relative_label = item["relative"]
            a_arrow, a_label = item["a"]

            set_vector(
                observer_arrow,
                observer_label,
                (0, 0),
                observer,
                observer_fraction,
                case["observer"],
            )
            set_vector(
                relative_arrow,
                relative_label,
                observer,
                relative,
                relative_fraction,
                case["relative"],
            )
            set_vector(
                a_arrow,
                a_label,
                (0, 0),
                CAR_A_VELOCITY,
                a_fraction,
                "v_A = 10 m/s east",
            )
            item["answer"].set_text(case["answer"] if frame >= 3 else "")
            changed.extend(
                (
                    observer_arrow,
                    observer_label,
                    relative_arrow,
                    relative_label,
                    a_arrow,
                    a_label,
                    item["answer"],
                )
            )
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
        repeat_delay=1600,
        blit=True,
        cache_frame_data=False,
    )
    figure._relative_velocity_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
