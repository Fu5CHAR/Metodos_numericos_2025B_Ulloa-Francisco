import numpy as np


def solar_vector(theta, alpha):
    """
    Vector unitario de radiación solar.
    """
    return np.array([
        np.cos(theta) * np.sin(alpha),
        np.cos(theta) * np.cos(alpha),
        np.sin(theta)
    ])


def panel_normal(pitch, roll):
    """
    Vector normal del panel solar.
    """
    return np.array([
        np.sin(roll) * np.cos(pitch),
        -np.sin(pitch),
        np.cos(roll) * np.cos(pitch)
    ])
