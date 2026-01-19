import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def panel_surface(normal, size=0.4):
    """
    Genera una superficie rectangular representando el panel solar.
    """
    n = normal / np.linalg.norm(normal)

    # Vector auxiliar cualquiera no colineal
    a = np.array([0, 0, 1]) if abs(n[2]) < 0.9 else np.array([1, 0, 0])

    v1 = np.cross(n, a)
    v1 /= np.linalg.norm(v1)
    v2 = np.cross(n, v1)

    corners = []
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            corners.append(dx * v1 * size + dy * v2 * size)

    return np.array(corners)

def plot_simulation(times, solar_vectors, panel_vectors):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlabel("Este")
    ax.set_ylabel("Norte")
    ax.set_zlabel("Arriba")

    ax.view_init(elev=25, azim=45)

    # Trayectoria solar
    sun_path, = ax.plot([], [], [], '--', color='orange', label="Trayectoria Solar")

    # Punto del sol
    sun_point = ax.scatter([], [], [], color='gold', s=80, label="Sol")

    # Trayectorias angulares
    az_line, = ax.plot([], [], [], '--', color='gray', label="Azimut")
    el_line, = ax.plot([], [], [], '--', color='purple', label="Elevación")
    pitch_line, = ax.plot([], [], [], '--', color='green', label="Pitch")
    roll_line, = ax.plot([], [], [], '--', color='red', label="Roll")

    # Panel (superficie)
    panel_poly = [None]


    time_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)
    ax.legend(loc="upper right")

    slider_ax = plt.axes([0.2, 0.02, 0.6, 0.03])
    slider = Slider(slider_ax, "Tiempo", 0, len(times) - 1, valinit=0, valstep=1)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D


# ============================================================
# CONTENEDOR MUTABLE PARA LA SUPERFICIE DEL PANEL
# ============================================================
panel_poly = [None]


# ============================================================
# FUNCIÓN DE ACTUALIZACIÓN (SLIDER)
# ============================================================
def update(val):
    i = int(slider.val)

    s = solar_vectors[i]
    p = panel_vectors[i]

    # --------------------------------------------------------
    # Trayectoria solar
    # --------------------------------------------------------
    sun_path.set_data(solar_vectors[:i + 1, 0], solar_vectors[:i + 1, 1])
    sun_path.set_3d_properties(solar_vectors[:i + 1, 2])

    # Sol (punto)
    sun_point._offsets3d = ([s[0]], [s[1]], [s[2]])

    # --------------------------------------------------------
    # Ángulos solares
    # --------------------------------------------------------
    # Azimut
    az_line.set_data([0, s[0]], [0, s[1]])
    az_line.set_3d_properties([0, 0])

    # Elevación
    el_line.set_data([s[0], s[0]], [s[1], s[1]])
    el_line.set_3d_properties([0, s[2]])

    # --------------------------------------------------------
    # Ángulos del panel
    # --------------------------------------------------------
    # Pitch
    pitch_line.set_data([0, p[0]], [0, 0])
    pitch_line.set_3d_properties([0, p[2]])

    # Roll
    roll_line.set_data([0, 0], [0, p[1]])
    roll_line.set_3d_properties([0, p[2]])

    # --------------------------------------------------------
    # Panel como superficie
    # --------------------------------------------------------
    if panel_poly[0] is not None:
        panel_poly[0].remove()

    surf = panel_surface(p)

    panel_poly[0] = ax.plot_trisurf(
        surf[:, 0],
        surf[:, 1],
        surf[:, 2],
        color="tab:blue",
        alpha=0.55
    )

    # --------------------------------------------------------
    # Texto de tiempo
    # --------------------------------------------------------
    time_text.set_text(times[i].strftime("Tiempo: %H:%M"))

    # --------------------------------------------------------
    # Ejes dinámicos (no fijos)
    # --------------------------------------------------------
    lim = 1.3
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(0, lim)

    fig.canvas.draw_idle()



    slider.on_changed(update)
    update(0)
    plt.show()
