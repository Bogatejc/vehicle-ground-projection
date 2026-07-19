from __future__ import annotations

import numpy as np


def rotation_matrix_z(angle: float) -> np.ndarray:
    """Rotation around global Z axis."""

    c = np.cos(angle)
    s = np.sin(angle)

    return np.array([[c, -s], [s, c]])


def antenna_offset_vehicle(
    roll: np.ndarray, pitch: np.ndarray, height: float
) -> np.ndarray:
    """
    Computes the antenna offset expressed in the vehicle frame.

    Parameters
    ----------
    roll : radians
    pitch : radians
    height : antenna height above moving plane (mm)

    Returns
    -------
    Nx2 array containing X, Y offset in vehicle frame.
    """

    dx = height * np.sin(pitch)
    dy = -height * np.sin(roll) * np.cos(pitch)

    return np.column_stack((dx, dy))


def project_to_ground(
    x: np.ndarray,
    y: np.ndarray,
    heading: np.ndarray,
    roll: np.ndarray,
    pitch: np.ndarray,
    height: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes projection of GNSS antenna onto moving plane.
    """

    offset = antenna_offset_vehicle(roll, pitch, height)
    dx, dy = offset[:, 0], offset[:, 1]

    cos_h = np.cos(heading)
    sin_h = np.sin(heading)

    ground_x = x - (dx * cos_h - dy * sin_h)
    ground_y = y - (dx * sin_h + dy * cos_h)

    return ground_x, ground_y
