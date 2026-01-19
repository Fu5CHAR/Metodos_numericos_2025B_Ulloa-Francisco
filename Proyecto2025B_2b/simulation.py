import numpy as np
from datetime import timedelta
from solar_position import getSolarPosition
from control_angles import compute_control_angles
from vectors import solar_vector, panel_normal


def simulate(
    start_date,
    duration_hours=12,
    step_minutes=10,
):
    """
    Simula la trayectoria solar y la orientación del panel.
    """
    times = []
    solar_vectors = []
    panel_vectors = []

    for i in range(0, duration_hours * 60, step_minutes):
        current_time = start_date + timedelta(minutes=i)
        az, el = getSolarPosition(date=current_time)

        if el > 0:
            pitch, roll = compute_control_angles(el, az)

            s = solar_vector(
                np.deg2rad(el),
                np.deg2rad(az)
            )
            n = panel_normal(pitch, roll)

            times.append(current_time)
            solar_vectors.append(s)
            panel_vectors.append(n)

    return times, np.array(solar_vectors), np.array(panel_vectors)
