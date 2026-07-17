from __future__ import annotations

import numpy as np
import pandas as pd

from geometry import project_to_ground
from heading import compute_heading
from visualization import (
    plot_projection_vectors,
    plot_results,
    plot_trajectory_with_heading,
)

ANTENNA_HEIGHT = 1500.0


def main():
    df = pd.read_csv("data/data.csv")

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

    result.to_csv("./output/solution.csv", index=False)

    plot_results(x, y, gx, gy, heading, df["time_s"].to_numpy(), roll, pitch)

    plot_trajectory_with_heading(x, y, gx, gy, heading)

    plot_projection_vectors(x, y, gx, gy)


if __name__ == "__main__":
    main()
