from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def plot_results(x, y, gx, gy, heading, time, roll, pitch):
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(x, y, label="GNSS")
    ax.plot(gx, gy, label="Ground projection")

    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.axis("equal")
    ax.grid(True)
    ax.legend()

    fig2, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, np.degrees(heading))
    ax.set_ylabel("Heading [deg]")
    ax.grid(True)

    fig3, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, np.degrees(roll), label="Roll")
    ax.plot(time, np.degrees(pitch), label="Pitch")
    ax.legend()
    ax.grid(True)

    plt.show()


def plot_trajectory_with_heading(
    x: np.ndarray,
    y: np.ndarray,
    ground_x: np.ndarray,
    ground_y: np.ndarray,
    heading: np.ndarray,
    step: int = 3,
) -> None:
    """
    Plot GNSS trajectory and projected trajectory with heading vectors.
    """

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.plot(
        x,
        y,
        label="GNSS trajectory",
        linewidth=2,
    )

    ax.plot(
        ground_x,
        ground_y,
        label="Ground projection",
        linewidth=2,
        linestyle="--",
    )

    # ax.quiver(
    #     x[::step],
    #     y[::step],
    #     np.cos(heading)[::step],
    #     np.sin(heading)[::step],
    #     angles="xy",
    #     scale_units="xy",
    #     scale=0.02,
    #     width=0.003,
    #     color="tab:red",
    #     label="Heading",
    # )

    arrow_length = 200.0  # mm

    u = arrow_length * np.cos(heading)
    v = arrow_length * np.sin(heading)

    ax.quiver(
        x[::step],
        y[::step],
        u[::step],
        v[::step],
        angles="xy",
        scale_units="xy",
        scale=1,
        width=0.003,
        color="tab:red",
        label="Heading",
    )

    ax.set_title("Vehicle Trajectory with Estimated Heading")
    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.set_aspect("equal")
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()


def plot_projection_vectors(
    x: np.ndarray,
    y: np.ndarray,
    ground_x: np.ndarray,
    ground_y: np.ndarray,
) -> None:
    """
    Plot vectors from the GNSS antenna position to its projection
    on the moving plane.
    """

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.plot(
        x,
        y,
        color="tab:blue",
        linewidth=2,
        label="GNSS trajectory",
    )

    ax.scatter(
        ground_x,
        ground_y,
        s=25,
        color="tab:orange",
        label="Ground projection",
    )

    for i in range(len(x)):
        ax.plot(
            [x[i], ground_x[i]],
            [y[i], ground_y[i]],
            color="gray",
            linewidth=1,
            alpha=0.6,
        )

    ax.set_title("GNSS Antenna Projection onto Moving Plane")
    ax.set_xlabel("X [mm]")
    ax.set_ylabel("Y [mm]")
    ax.set_aspect("equal")
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()
