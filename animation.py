from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

VEHICLE_LENGTH_MM = 400.0
VEHICLE_WIDTH_MM = 250.0
TRAJECTORY_ARROW_LENGTH_MM = 260.0
VEHICLE_ARROW_LENGTH_MM = 300.0
TRAJECTORY_ARROW_WIDTH = 0.0025
VEHICLE_ARROW_WIDTH = 0.016


def rotate_points(points: np.ndarray, angle: float) -> np.ndarray:
    """Rotate a set of 2D points around the origin by an angle in radians."""

    rotation = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]],
        dtype=float,
    )
    return points @ rotation.T


def create_vehicle_outline(
    length: float = VEHICLE_LENGTH_MM,
    width: float = VEHICLE_WIDTH_MM,
) -> np.ndarray:
    """Create the polygon coordinates of a simple vehicle body."""

    return np.array(
        [
            [-length / 2.0, -width / 2.0],
            [length / 2.0, -width / 2.0],
            [length / 2.0, width / 2.0],
            [-length / 2.0, width / 2.0],
            [-length / 2.0, -width / 2.0],
        ],
        dtype=float,
    )


def compute_attitude_line(
    angle: float,
    length: float = 1.0,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return start and end points for a centered attitude line."""

    points = np.array([[-length, 0.0], [length, 0.0]], dtype=float)
    rotated = rotate_points(points, -angle)
    return (float(rotated[0, 0]), float(rotated[0, 1])), (
        float(rotated[1, 0]),
        float(rotated[1, 1]),
    )


def update_information_panel(
    text_artist: object,
    sample_index: int,
    time_value: float,
    heading_value: float,
    roll_value: float,
    pitch_value: float,
    antenna_height: float,
) -> None:
    """Refresh the text content shown in the information panel."""

    heading_deg = np.degrees(heading_value)
    roll_deg = np.degrees(roll_value)
    pitch_deg = np.degrees(pitch_value)

    content = (
        "Current Sample\n\n"
        f"Sample: {sample_index}\n"
        f"Time: {time_value:.2f} s\n"
        f"Heading: {heading_deg:.1f}°\n"
        f"Roll: {roll_deg:+.2f}°\n"
        f"Pitch: {pitch_deg:+.2f}°\n"
        f"Antenna height: {antenna_height:.0f} mm"
    )
    text_artist.set_text(content)


def create_animation(
    time: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    ground_x: np.ndarray,
    ground_y: np.ndarray,
    heading: np.ndarray,
    roll: np.ndarray,
    pitch: np.ndarray,
    filename: str = "vehicle_motion.gif",
) -> None:
    """Create a polished, multi-panel animation of vehicle motion and attitude."""

    time = np.asarray(time, dtype=float)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ground_x = np.asarray(ground_x, dtype=float)
    ground_y = np.asarray(ground_y, dtype=float)
    heading = np.asarray(heading, dtype=float)
    roll = np.asarray(roll, dtype=float)
    pitch = np.asarray(pitch, dtype=float)

    if not all(
        array.shape[0] == time.shape[0]
        for array in (x, y, ground_x, ground_y, heading, roll, pitch)
    ):
        raise ValueError("All input arrays must have the same length.")

    fig = plt.figure(figsize=(14, 8), constrained_layout=True)
    gs = fig.add_gridspec(
        2,
        3,
        width_ratios=[1.6, 1.0, 1.0],
        wspace=0.22,
        hspace=0.24,
    )

    ax_trajectory = fig.add_subplot(gs[:, 0])
    ax_vehicle = fig.add_subplot(gs[0, 1])
    ax_info = fig.add_subplot(gs[0, 2])
    ax_pitch = fig.add_subplot(gs[1, 1])
    ax_roll = fig.add_subplot(gs[1, 2])

    for axis in (ax_trajectory, ax_vehicle, ax_pitch, ax_roll):
        axis.set_facecolor("#fbfbfb")

    ax_info.set_facecolor("#f5f7fa")

    ax_trajectory.plot(
        x,
        y,
        color="#4c78a8",
        linewidth=1.8,
        alpha=0.45,
        label="GNSS path",
    )
    ax_trajectory.plot(
        ground_x,
        ground_y,
        color="#f58518",
        linewidth=1.8,
        alpha=0.45,
        label="Ground projection",
    )

    (gnss_point,) = ax_trajectory.plot(
        [],
        [],
        marker="o",
        markersize=8,
        color="#4c78a8",
        markerfacecolor="#4c78a8",
        markeredgecolor="white",
        markeredgewidth=0.7,
        label="GNSS",
    )
    (ground_point,) = ax_trajectory.plot(
        [],
        [],
        marker="x",
        markersize=8,
        color="#f58518",
        markeredgewidth=2.0,
        label="Ground projection",
    )

    heading_arrow = ax_trajectory.quiver(
        [x[0]],
        [y[0]],
        [0.0],
        [0.0],
        angles="xy",
        scale_units="xy",
        scale=1.0,
        width=TRAJECTORY_ARROW_WIDTH,
        color="#2f2f2f",
    )

    ax_trajectory.set_title("Vehicle trajectory", fontsize=12, fontweight="bold")
    ax_trajectory.set_xlabel("X [mm]")
    ax_trajectory.set_ylabel("Y [mm]")
    ax_trajectory.set_aspect("equal")
    ax_trajectory.grid(True, alpha=0.35)
    ax_trajectory.legend(loc="best", frameon=True, facecolor="white")

    vehicle_outline = create_vehicle_outline()
    (vehicle_line,) = ax_vehicle.plot([], [], color="#1f77b4", linewidth=3.0)
    vehicle_arrow = ax_vehicle.quiver(
        [0.0],
        [0.0],
        [0.0],
        [0.0],
        angles="xy",
        scale_units="xy",
        scale=1.0,
        width=VEHICLE_ARROW_WIDTH,
        color="#e45756",
    )

    ax_vehicle.set_xlim(-450.0, 450.0)
    ax_vehicle.set_ylim(-450.0, 450.0)
    ax_vehicle.set_aspect("equal")
    ax_vehicle.grid(True, alpha=0.35)
    ax_vehicle.set_title("Vehicle orientation", fontsize=12, fontweight="bold")

    pitch_start, pitch_end = compute_attitude_line(0.0, length=1.0)
    pitch_arrow = ax_pitch.annotate(
        "",
        xy=pitch_end,
        xytext=pitch_start,
        arrowprops=dict(
            arrowstyle="-|>",
            linewidth=2.4,
            color="#4c78a8",
            mutation_scale=24,
            shrinkA=0,
            shrinkB=0,
        ),
    )
    pitch_text = ax_pitch.text(
        0.0,
        -0.9,
        "",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
    ax_pitch.set_xlim(-1.4, 1.4)
    ax_pitch.set_ylim(-1.1, 1.1)
    ax_pitch.set_aspect("equal")
    ax_pitch.grid(True, alpha=0.35)
    ax_pitch.set_title("Pitch", fontsize=12, fontweight="bold")

    (roll_line,) = ax_roll.plot([], [], color="#f58518", linewidth=2.6)
    roll_text = ax_roll.text(
        0.0,
        -0.9,
        "",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
    )
    ax_roll.set_xlim(-1.4, 1.4)
    ax_roll.set_ylim(-1.1, 1.1)
    ax_roll.set_aspect("equal")
    ax_roll.grid(True, alpha=0.35)
    ax_roll.set_title("Roll", fontsize=12, fontweight="bold")

    info_text = ax_info.text(
        0.04,
        0.96,
        "",
        ha="left",
        va="top",
        transform=ax_info.transAxes,
        fontsize=11,
        linespacing=1.45,
        fontfamily="monospace",
    )
    ax_info.set_axis_off()

    def update(frame: int) -> tuple[object, ...]:
        gnss_point.set_data([x[frame]], [y[frame]])
        ground_point.set_data([ground_x[frame]], [ground_y[frame]])

        heading_arrow.set_offsets([[x[frame], y[frame]]])
        heading_arrow.set_UVC(
            np.cos(heading[frame]) * TRAJECTORY_ARROW_LENGTH_MM,
            np.sin(heading[frame]) * TRAJECTORY_ARROW_LENGTH_MM,
        )

        rotated_vehicle = rotate_points(vehicle_outline, heading[frame])
        vehicle_line.set_data(rotated_vehicle[:, 0], rotated_vehicle[:, 1])
        vehicle_arrow.set_UVC(
            np.cos(heading[frame]) * VEHICLE_ARROW_LENGTH_MM,
            np.sin(heading[frame]) * VEHICLE_ARROW_LENGTH_MM,
        )

        pitch_start, pitch_end = compute_attitude_line(pitch[frame], length=1.0)
        pitch_arrow.xy = pitch_end
        pitch_arrow.set_position(pitch_start)
        pitch_text.set_text(f"Pitch: {np.degrees(pitch[frame]):+.2f}°")

        roll_start, roll_end = compute_attitude_line(roll[frame], length=1.0)
        roll_line.set_data([roll_start[0], roll_end[0]], [roll_start[1], roll_end[1]])
        roll_text.set_text(f"Roll: {np.degrees(roll[frame]):+.2f}°")

        update_information_panel(
            info_text,
            frame,
            time[frame],
            heading[frame],
            roll[frame],
            pitch[frame],
            antenna_height=1500.0,
        )

        return (
            gnss_point,
            ground_point,
            heading_arrow,
            vehicle_line,
            vehicle_arrow,
            pitch_arrow,
            pitch_text,
            roll_line,
            roll_text,
            info_text,
        )

    animation = FuncAnimation(
        fig,
        update,
        frames=len(time),
        interval=300,
        blit=False,
    )
    animation.save(filename, writer=PillowWriter(fps=4))
    plt.close(fig)
