import pandas as pd
import os

# Ruta de la carpeta donde está el CSV
ruta = r'C:\Users\pc\Videos\2025B\metodos_numericos\Metodos_numericos_2025B_Ulloa-Francisco\Proyecto2025B2\output'

print(f"¿Existe la carpeta?: {os.path.exists(ruta)}")

# Listar archivos dentro de la carpeta output
archivos = os.listdir(ruta)
print("Archivos en la carpeta output:")
for archivo in archivos:
    print(archivo)

# Ruta completa del archivo CSV
ruta_completa = os.path.join(ruta, 'elev_all_hgts.csv')

print(f"¿Existe el archivo CSV?: {os.path.exists(ruta_completa)}")

# Leer el CSV
df = pd.read_csv(ruta_completa)

# Mostrar las primeras filas
print(df.tail(500))




