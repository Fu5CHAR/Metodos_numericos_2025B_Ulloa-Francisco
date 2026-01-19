import numpy as np


def compute_control_angles(elevation_deg, azimuth_deg):
    """
    Calcula los ángulos de control (pitch, roll) del seguidor solar.

    Parameters
    ----------
    elevation_deg : float
        Elevación solar (θ) en grados
    azimuth_deg : float
        Azimut solar (α) en grados

    Returns
    -------
    pitch : float
        Ángulo pitch en radianes
    roll : float
        Ángulo roll en radianes
    """
    theta = np.deg2rad(elevation_deg)
    alpha = np.deg2rad(azimuth_deg)

    pitch = -np.arcsin(np.cos(theta) * np.cos(alpha))
    roll = np.arctan2(
        np.cos(theta) * np.sin(alpha),
        np.sin(theta)
    )

    return pitch, roll
