from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from constants import ANTENNA_HEIGHT
from geometry import project_to_ground
from heading import compute_heading


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the vehicle projection workflow."""

    parser = argparse.ArgumentParser(
        description="Compute vehicle heading and ground projection"
    )
    parser.add_argument(
        "input_path",
        nargs="?",
        default="data/data.csv",
        help="Path to the input CSV file (default: data/data.csv)",
    )
    parser.add_argument(
        "--plots",
        action="store_true",
        help="Show the static visualization plots",
    )
    parser.add_argument(
        "--gif",
        action="store_true",
        help="Generate the animated GIF",
    )
    parser.add_argument(
        "--output",
        default="./output/solution.csv",
        help="Path to save the processed solution CSV",
    )
    return parser.parse_args()


def main(
    input_path: str = "data/data.csv",
    plots: bool = False,
    gif: bool = False,
    output: str = "./output/solution.csv",
) -> None:
    """Run the vehicle projection and heading workflow."""

    df = pd.read_csv(input_path)

    roll = np.deg2rad(df["roll_deg"].to_numpy())
    pitch = np.deg2rad(df["pitch_deg"].to_numpy())

    x = df["x_mm"].to_numpy(dtype=float)
    y = df["y_mm"].to_numpy(dtype=float)

    heading = compute_heading(x, y)

    gx, gy = project_to_ground(x, y, heading, roll, pitch, ANTENNA_HEIGHT)

    result = df.copy()

    result["heading_deg"] = np.rad2deg(heading)
    result["ground_x_mm"] = gx
    result["ground_y_mm"] = gy

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    if plots:
        from visualization import (
            plot_projection_vectors,
            plot_results,
            plot_trajectory_with_heading,
        )

        plot_results(x, y, gx, gy, heading, df["time_s"].to_numpy(), roll, pitch)
        plot_trajectory_with_heading(x, y, gx, gy, heading)
        plot_projection_vectors(x, y, gx, gy)

    if gif:
        from animation import create_animation

        create_animation(
            time=df["time_s"].to_numpy(),
            x=x,
            y=y,
            ground_x=gx,
            ground_y=gy,
            heading=heading,
            roll=roll,
            pitch=pitch,
            filename="vehicle_motion.gif",
        )


if __name__ == "__main__":
    args = parse_args()
    main(input_path=args.input_path, plots=args.plots, gif=args.gif, output=args.output)
