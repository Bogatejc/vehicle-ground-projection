from __future__ import annotations

import numpy as np


def compute_heading(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Estimates vehicle heading using central differences.

    Returns heading in radians.
    """

    dx = np.empty_like(x, dtype=float)
    dy = np.empty_like(y, dtype=float)

    dx[1:-1] = x[2:] - x[:-2]
    dy[1:-1] = y[2:] - y[:-2]

    dx[0] = x[1] - x[0]
    dy[0] = y[1] - y[0]

    dx[-1] = x[-1] - x[-2]
    dy[-1] = y[-1] - y[-2]

    heading = np.arctan2(dy, dx)
    heading = np.unwrap(heading)

    return heading
