from datetime import datetime
from matplotlib.widgets import Slider
from pytz import timezone

from simulation import simulate
from visualization import plot_simulation, update


def main():
    # ===============================
    # Parámetros de simulación
    # ===============================
    start_date = datetime(
        2025, 6, 21, 6, 0,
        tzinfo=timezone("America/Guayaquil")
    )

    duration_hours = 12     # Duración total de la simulación
    step_minutes = 10       # Resolución temporal

    # ===============================
    # Ejecución de la simulación
    # ===============================
    times, solar_vectors, panel_vectors = simulate(
        start_date=start_date,
        duration_hours=duration_hours,
        step_minutes=step_minutes
    )

    if len(times) == 0:
        raise RuntimeError(
            "La simulación no generó datos: el Sol no estuvo sobre el horizonte."
        )

    # ===============================
    # Visualización interactiva
    # ===============================
    slider = Slider(
        ax_slider,
        "Tiempo",
        0,
        len(times) - 1,
        valinit=0,
    valstep=1
)

slider.on_changed(update)

# IMPORTANTE: inicializar visualización
update(0)

plt.show()



if __name__ == "__main__":
    main()

