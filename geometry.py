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

    local_offset = antenna_offset_vehicle(roll, pitch, height)
    ground = np.zeros_like(local_offset)

    for i in range(len(x)):
        R = rotation_matrix_z(heading[i])
        ground[i] = R @ local_offset[i]

    ground_x = x - ground[:, 0]
    ground_y = y - ground[:, 1]

    return ground_x, ground_y
