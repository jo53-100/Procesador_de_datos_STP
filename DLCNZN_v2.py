# Crea un archivo sin la ultima columna y sin ceros, filtra archivos vacíos y reemplaza numeros restantes por 1
# nombra todo con sufijo '_DLCNZN1'
# Idealmente este es el paso 1 & 2 & 3 & 4

import pandas as pd
import numpy as np
import os
import sys

def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} no es un directorio válido.")
        return

    # Toma el nombre del folder y crea uno nuevo con el sufijo '_DLCNZN1'
    folder_name = os.path.basename(folder_path.rstrip('/'))
    new_folder_name = f"{folder_name}_DLCNZN1"
    new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

    # Crea un nuevo folder si no existe
    os.makedirs(new_folder_path, exist_ok=True)

    # Lista todos los archivos en el folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not files:
        print("No hay archivos CSV en el folder especificado.")
        return

    # Hace un bucle en cada archivo
    for file in files:
        file_path = os.path.join(folder_path, file)

        file_name, file_extension = os.path.splitext(file)
        new_file = os.path.join(new_folder_path, f"{file_name}_DLCNZN1{file_extension}")

        try:
            # Lee el CSV
            df = pd.read_csv(file_path)

            # Suelta la última columna
            df = df.iloc[:, :-1]

            # Elimina filas que contienen ceros
            df = df[(df != 0).all(axis=1)]

            # Verifica si el DataFrame está vacío después de las operaciones
            if not df.empty:
                # Reemplaza todos los números restantes por 1 usando una función vectorizada de NumPy
                df[df.select_dtypes(include=[np.number]).columns] = 1

                # Guarda el DataFrame modificado a un nuevo archivo
                df.to_csv(new_file, index=False)

                print(f"El archivo {file} fue procesado y guardado como {new_file}")

        except Exception as e:
            print(f"Error procesando {file}: {e}")

if __name__ == "__main__":
    # Revisa si el folder de entrada es dado como argumento de línea
    if len(sys.argv) < 2:
        # Si no fue dado pide input
        folder_path = input("Introduce la ruta al folder con los archivos CSV: ").strip()
        folder_path = folder_path.strip('"').strip("'")
    else:
        # Usa el argumento de línea como ruta del folder de entrada
        folder_path = sys.argv[1].strip()
    # Llama la primera función
    process_folder(folder_path)
