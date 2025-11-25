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

        def valor_final(i_p):
            if abs(i_p) < 1e-12:
                return V0 + A * n
            return V0 * (1 + i_p) ** n + A * (((1 + i_p) ** n - 1) / i_p)

        # Búsqueda por bisección
        low, high = 0.0, 1.0
        f_low, f_high = valor_final(low), valor_final(high)

        expand_count = 0
        while f_high < Vf and expand_count < 50:
            high *= 2
            f_high = valor_final(high)
            expand_count += 1

        if f_low > Vf:
            messagebox.showerror("Error", "Con i_p = 0 ya se supera el valor final deseado.")
            return

        i_p_mid = None
        for _ in range(100):
            mid = (low + high) / 2
            f_mid = valor_final(mid)
            if f_mid < Vf:
                low = mid
            else:
                high = mid
            i_p_mid = mid

        # Tasa anual efectiva
        tasa_anual_efectiva = (1 + i_p_mid) ** periodos_anuales - 1
        tasa_anual_percent = tasa_anual_efectiva * 100

        label_resultado.config(
            text=f"Tasa de interés anual estimada: {tasa_anual_percent:.2f}%"
        )

        # Calcular tabla de evolución
        saldo = V0
        datos_tabla = []
        for t in range(1, n + 1):
            interes = saldo * i_p_mid
            saldo_final = saldo + interes + A
            datos_tabla.append((t, saldo, A, interes, saldo_final))
            saldo = saldo_final

        # Limpiar tabla anterior
        for i in tabla.get_children():
            tabla.delete(i)

        # Insertar nueva tabla
        for fila in datos_tabla:
            tabla.insert("", "end", values=[f"{x:.2f}" if isinstance(x, float) else x for x in fila])

        # Graficar resultados
        graficar_evolucion(datos_tabla, tasa_anual_percent)

        # Guardar en JSON
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

    # Crear figura
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(periodos, saldos, marker="o")
    ax.set_title(f"Evolución del saldo (Tasa anual {tasa:.2f}%)")
    ax.set_xlabel("Período")
    ax.set_ylabel("Saldo ($)")
    ax.grid(True)

    # Mostrar gráfico en ventana
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# ===================== INTERFAZ =====================

root = tk.Tk()
root.title("Calculadora de Tasa de Interés Anual")
root.geometry("800x600")
root.resizable(False, False)

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
