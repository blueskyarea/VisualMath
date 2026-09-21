"""摩擦により小物体と台が同じ速さになる過程を可視化する。"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch, Rectangle


MASS_PLATFORM = 1.4
MASS_BLOCK = 0.60
INITIAL_BLOCK_SPEED = 0.70
MU_K = 0.25
GRAVITY = 9.8
FRICTION = MU_K * MASS_BLOCK * GRAVITY
ACCELERATION_PLATFORM = FRICTION / MASS_PLATFORM
ACCELERATION_BLOCK = -FRICTION / MASS_BLOCK
COMMON_SPEED = MASS_BLOCK * INITIAL_BLOCK_SPEED / (MASS_PLATFORM + MASS_BLOCK)
SLIDING_TIME = INITIAL_BLOCK_SPEED / (ACCELERATION_PLATFORM - ACCELERATION_BLOCK)
APPROACH_TIME = 0.80
PLATFORM_START = 0.0
BLOCK_CONTACT_POSITION = -1.75
TOTAL_TIME = APPROACH_TIME + SLIDING_TIME + 0.40


def add_arrow(axis, color):
    arrow = FancyArrowPatch(
        (0, 0),
        (0, 0),
        arrowstyle="->",
        mutation_scale=14,
        linewidth=2.4,
        color=color,
    )
    axis.add_patch(arrow)
    return arrow


def set_arrow(arrow, start, vector):
    arrow.set_positions(start, (start[0] + vector[0], start[1] + vector[1]))


def positions_and_speeds(time):
    """地面から見た A, B の位置と速度を返す。"""
    if time <= APPROACH_TIME:
        # B は左側の固定面を進み、台 A に乗り移る直前である。
        platform_x = PLATFORM_START
        block_x = BLOCK_CONTACT_POSITION - INITIAL_BLOCK_SPEED * (APPROACH_TIME - time)
        platform_v = 0.0
        block_v = INITIAL_BLOCK_SPEED
    else:
        sliding_elapsed = time - APPROACH_TIME
        if sliding_elapsed <= SLIDING_TIME:
            platform_x = PLATFORM_START + ACCELERATION_PLATFORM * sliding_elapsed**2 / 2
            block_x = (
                BLOCK_CONTACT_POSITION
                + INITIAL_BLOCK_SPEED * sliding_elapsed
                + ACCELERATION_BLOCK * sliding_elapsed**2 / 2
            )
            platform_v = ACCELERATION_PLATFORM * sliding_elapsed
            block_v = INITIAL_BLOCK_SPEED + ACCELERATION_BLOCK * sliding_elapsed
        else:
            platform_at_join = PLATFORM_START + ACCELERATION_PLATFORM * SLIDING_TIME**2 / 2
            block_at_join = (
                BLOCK_CONTACT_POSITION
                + INITIAL_BLOCK_SPEED * SLIDING_TIME
                + ACCELERATION_BLOCK * SLIDING_TIME**2 / 2
            )
            elapsed = sliding_elapsed - SLIDING_TIME
            platform_x = platform_at_join + COMMON_SPEED * elapsed
            block_x = block_at_join + COMMON_SPEED * elapsed
            platform_v = COMMON_SPEED
            block_v = COMMON_SPEED
    return platform_x, block_x, platform_v, block_v


def main(interval_ms=50):
    frame_count = 120
    times = [TOTAL_TIME * index / frame_count for index in range(frame_count + 1)]
    platform_speeds = [positions_and_speeds(time)[2] for time in times]
    block_speeds = [positions_and_speeds(time)[3] for time in times]

    figure, (motion_axis, speed_axis) = plt.subplots(1, 2, figsize=(13, 6))
    figure.suptitle("A block and a platform become one moving system")

    # 左: 台と小物体の運動
    motion_axis.axhline(0, color="#334155", linewidth=2)
    motion_axis.text(-3.6, -0.3, "smooth floor", color="#334155")
    motion_axis.plot((-3.5, -2.0), (0.50, 0.50), color="#475569", linewidth=4)
    motion_axis.text(-3.45, 0.67, "fixed horizontal surface", color="#475569", fontsize=8.5)
    motion_axis.set_xlim(-3.8, 2.8)
    motion_axis.set_ylim(-0.5, 1.6)
    motion_axis.set_aspect("equal")
    motion_axis.set_title("Motion and kinetic friction")
    motion_axis.set_xlabel("horizontal position [m]")
    motion_axis.set_yticks([])
    motion_axis.grid(alpha=0.2)
    platform = Rectangle((-2, 0.15), 4.0, 0.35, color="#64748b")
    block = Rectangle((-1.45, 0.50), 0.50, 0.45, color="#2563eb")
    motion_axis.add_patch(platform)
    motion_axis.add_patch(block)
    motion_axis.text(-0.15, 0.23, "platform A", color="white", fontsize=9)
    friction_on_block = add_arrow(motion_axis, "#dc2626")
    friction_on_platform = add_arrow(motion_axis, "#16a34a")
    motion_info = motion_axis.text(
        0.03,
        0.96,
        "",
        transform=motion_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    # 右: 速度と時刻の関係
    speed_axis.plot(times, platform_speeds, color="#64748b", label="platform A")
    speed_axis.plot(times, block_speeds, color="#2563eb", label="block B")
    speed_axis.axvline(APPROACH_TIME, color="#f59e0b", linestyle="--")
    speed_axis.axvline(APPROACH_TIME + SLIDING_TIME, color="#dc2626", linestyle="--")
    speed_axis.axhline(COMMON_SPEED, color="#16a34a", linestyle="--")
    speed_axis.set_title("Velocity-time graph")
    speed_axis.set_xlabel("time [s]")
    speed_axis.set_ylabel("velocity [m/s]")
    speed_axis.set_ylim(-0.05, 0.80)
    speed_axis.grid(alpha=0.2)
    speed_axis.legend()
    point_platform, = speed_axis.plot([], [], marker="o", color="#64748b", markersize=7)
    point_block, = speed_axis.plot([], [], marker="o", color="#2563eb", markersize=7)
    speed_info = speed_axis.text(
        0.03,
        0.95,
        "",
        transform=speed_axis.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    def update(frame):
        time = times[frame]
        platform_x, block_x, platform_v, block_v = positions_and_speeds(time)
        platform.set_x(platform_x - 2.0)
        block.set_x(block_x - 0.25)
        point_platform.set_data([time], [platform_v])
        point_block.set_data([time], [block_v])

        if time < APPROACH_TIME:
            friction_on_block.set_visible(False)
            friction_on_platform.set_visible(False)
            motion_info.set_text(
                "before transfer\n"
                "B moves on the fixed surface\n"
                "A remains at rest\n"
                "no friction between A and B yet"
            )
        elif time < APPROACH_TIME + SLIDING_TIME:
            # B は A より右へ滑るため、B には左向き、A には右向きの摩擦力がはたらく。
            set_arrow(friction_on_block, (block_x, 1.15), (-0.55, 0))
            set_arrow(friction_on_platform, (platform_x, 0.62), (0.55, 0))
            friction_on_block.set_visible(True)
            friction_on_platform.set_visible(True)
            motion_info.set_text(
                "sliding\n"
                "friction on B: left\n"
                "friction on A: right\n"
                f"kinetic friction = {FRICTION:.2f} N"
            )
        else:
            friction_on_block.set_visible(False)
            friction_on_platform.set_visible(False)
            motion_info.set_text(
                "no relative motion\n"
                "A and B move together\n"
                f"common speed = {COMMON_SPEED:.2f} m/s"
            )

        speed_info.set_text(
            "horizontal momentum is conserved\n"
            f"0.60 x 0.70 = (1.4 + 0.60)V\n"
            f"V = {COMMON_SPEED:.2f} m/s\n"
            f"transfer at t = {APPROACH_TIME:.2f} s\n"
            f"same speed after {SLIDING_TIME:.2f} s of sliding"
        )
        return (
            platform,
            block,
            friction_on_block,
            friction_on_platform,
            motion_info,
            point_platform,
            point_block,
            speed_info,
        )

    def init():
        return update(0)

    animation = FuncAnimation(
        figure,
        update,
        init_func=init,
        frames=range(frame_count + 1),
        interval=interval_ms,
        repeat=True,
        repeat_delay=1800,
        blit=True,
        cache_frame_data=False,
    )
    figure._block_platform_friction_animation = animation
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
