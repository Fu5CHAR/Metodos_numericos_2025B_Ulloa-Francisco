import json
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ARCHIVO_JSON = "escenarios_ahorro.json"

def guardar_json(datos):
    """Guarda los datos del escenario en un archivo JSON."""
    try:
        with open(ARCHIVO_JSON, "r") as f:
            escenarios = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        escenarios = []

    escenarios.append(datos)

    with open(ARCHIVO_JSON, "w") as f:
        json.dump(escenarios, f, indent=4)


def calcular_tasa_y_tabla():
    """Calcula la tasa de interés anual y genera la tabla de evolución."""
    try:
        nombre = entry_nombre.get().strip()
        V0 = float(entry_deposito.get())
        Vf = float(entry_final.get())
        A = float(entry_aporte.get())
        n = int(entry_duracion.get())
        periodo = combo_periodo.get().lower()

        if not nombre:
            messagebox.showerror("Error", "Por favor ingresa un nombre de usuario.")
            return

        # Periodos anuales según selección
        if periodo == "semanal":
            periodos_anuales = 52
        elif periodo == "mensual":
            periodos_anuales = 12
        elif periodo == "bimestral":
            periodos_anuales = 6
        elif periodo == "trimestral":
            periodos_anuales = 4
        else:
            messagebox.showerror("Error", "Selecciona un periodo válido.")
            return

        # =================================
        # NUEVAS FUNCIONES: vf, f, bisección
        # =================================

        def vf_given_i(i_p):
            """Calcula S_n usando aportes al inicio y luego interés cada periodo."""
            S = 0.0
            for t in range(1, n + 1):
                aporte = V0 if t == 1 else A
                S = (S + aporte) * (1 + i_p)
            return S

        def f(i_p):
            """Función objetivo para encontrar i_p."""
            return vf_given_i(i_p) - Vf

        def find_rate_bisection(a=0.0, b=1.0, tol=1e-12, maxiter=200):
            """Método de la bisección para encontrar la tasa periódica."""
            fa = f(a)
            fb = f(b)

            # Intento de expandir límite superior si no hay cambio de signo
            expand_count = 0
            while fa * fb > 0 and expand_count < 50:
                b *= 2
                fb = f(b)
                expand_count += 1

            if fa * fb > 0:
                messagebox.showerror("Error", "No se encontró intervalo válido para bisección.")
                return None

            # Bisección
            for _ in range(maxiter):
                m = (a + b) / 2
                fm = f(m)
                if abs(fm) < tol or (b - a) / 2 < tol:
                    return m
                if fa * fm < 0:
                    b, fb = m, fm
                else:
                    a, fa = m, fm

            return m  # último valor

        # =================================
        # Calcular tasa periódica i_p
        # =================================

        i_p_mid = find_rate_bisection()
        if i_p_mid is None:
            return

        # Tasa anual efectiva
        tasa_anual_efectiva = (1 + i_p_mid) ** periodos_anuales - 1
        tasa_anual_percent = tasa_anual_efectiva * 100

        label_resultado.config(
            text=f"Tasa de interés anual estimada: {tasa_anual_percent:.2f}%"
        )

        # ==============================
        # CREAR TABLA DE EVOLUCIÓN
        # ==============================

        saldo = 0.0
        datos_tabla = []

        for t in range(1, n + 1):
            aporte = V0 if t == 1 else A
            capital = saldo + aporte
            interes = capital * i_p_mid
            saldo_final = capital + interes

            datos_tabla.append((t, capital, aporte, interes, saldo_final))
            saldo = saldo_final

        # ==============================
        # Mostrar tabla en interfaz
        # ==============================

        for i in tabla.get_children():
            tabla.delete(i)

        for fila in datos_tabla:
            tabla.insert("", "end", values=[
                fila[0],
                f"{fila[1]:.2f}",
                f"{fila[2]:.2f}",
                f"{fila[3]:.2f}",
                f"{fila[4]:.2f}"
            ])

        # ==============================
        # Graficar evolución
        # ==============================

        graficar_evolucion(datos_tabla, tasa_anual_percent)

        # ==============================
        # Guardar JSON
        # ==============================

        guardar_json({
            "usuario": nombre,
            "deposito_inicial": V0,
            "valor_final_deseado": Vf,
            "aporte": A,
            "periodo": periodo,
            "duracion": n,
            "tasa_interes_anual": round(tasa_anual_percent, 4)
        })

    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos.")


def graficar_evolucion(datos_tabla, tasa):
    """Genera las gráficas en la interfaz."""
    periodos = [fila[0] for fila in datos_tabla]
    saldos = [fila[4] for fila in datos_tabla]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(periodos, saldos, marker="o")
    ax.set_title(f"Evolución del saldo (Tasa anual {tasa:.2f}%)")
    ax.set_xlabel("Período")
    ax.set_ylabel("Saldo ($)")
    ax.grid(True)

    for widget in frame_grafica.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# ===================== INTERFAZ =====================

root = tk.Tk()
root.title("Calculadora de Tasa de Interés Anual")
root.geometry("900x650")
root.resizable(True, True)

frame_izq = ttk.Frame(root, padding="15")
frame_izq.pack(side="left", fill="y")

frame_der = ttk.Frame(root, padding="15")
frame_der.pack(side="right", fill="both", expand=True)

# Campos de entrada
ttk.Label(frame_izq, text="Nombre del usuario:").grid(row=0, column=0, sticky="w", pady=3)
entry_nombre = ttk.Entry(frame_izq)
entry_nombre.grid(row=0, column=1, pady=3)

ttk.Label(frame_izq, text="Depósito inicial ($):").grid(row=1, column=0, sticky="w", pady=3)
entry_deposito = ttk.Entry(frame_izq)
entry_deposito.grid(row=1, column=1, pady=3)

ttk.Label(frame_izq, text="Valor final deseado ($):").grid(row=2, column=0, sticky="w", pady=3)
entry_final = ttk.Entry(frame_izq)
entry_final.grid(row=2, column=1, pady=3)

ttk.Label(frame_izq, text="Aporte por período ($):").grid(row=3, column=0, sticky="w", pady=3)
entry_aporte = ttk.Entry(frame_izq)
entry_aporte.grid(row=3, column=1, pady=3)

ttk.Label(frame_izq, text="Duración (n períodos):").grid(row=4, column=0, sticky="w", pady=3)
entry_duracion = ttk.Entry(frame_izq)
entry_duracion.grid(row=4, column=1, pady=3)

ttk.Label(frame_izq, text="Periodo de aporte:").grid(row=5, column=0, sticky="w", pady=3)
combo_periodo = ttk.Combobox(frame_izq, values=["Semanal", "Mensual", "Bimestral", "Trimestral"])
combo_periodo.grid(row=5, column=1, pady=3)
combo_periodo.current(0)

ttk.Button(frame_izq, text="Calcular tasa y tabla", command=calcular_tasa_y_tabla).grid(
    row=6, column=0, columnspan=2, pady=10
)

label_resultado = ttk.Label(frame_izq, text="", font=("Arial", 11, "bold"), foreground="blue")
label_resultado.grid(row=7, column=0, columnspan=2, pady=10)

# Tabla de resultados
cols = ("Periodo", "Saldo inicial", "Aporte", "Interés", "Saldo final")
tabla = ttk.Treeview(frame_der, columns=cols, show="headings", height=10)
for c in cols:
    tabla.heading(c, text=c)
    tabla.column(c, width=110, anchor="center")
tabla.pack(pady=10, fill="x")

# Frame para la gráfica
frame_grafica = ttk.Frame(frame_der)
frame_grafica.pack(fill="both", expand=True)

root.mainloop()




