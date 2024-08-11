#Borra la primera fila, este script se usa cuando tuviste que convertir el archivo de .xslx a .csv
#Guarda los archivos procesados con el sufijo '_FRD'
#Idealmente este es el paso 0.5

import os
import sys

import pandas as pd

def delete_first_row_and_save_new_folder(folder_path):
    # Revisa si el folder existe
    if not os.path.isdir(folder_path):
        print(f"El folder '{folder_path}' no existe.")
        return

    # Obtiene el nombre del folder y crea uno nuevo con el sufijo '_FDR'
    folder_name = os.path.basename(folder_path.rstrip('/'))
    new_folder_name = f"{folder_name}_FRD"
    new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

    # Crea el nuevo folder si no existe
    os.makedirs(new_folder_path, exist_ok=True)

    # Lista todos los CSV en el folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Hace un bucle en cada archivo
    for file_name in csv_files:
        original_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(new_folder_path, file_name)

        try:
            # Lee el archivo omitiendo la primera fila
            df = pd.read_csv(original_file_path, skiprows=1)

            # Guarda el DataFrame en un nuevo folder
            df.to_csv(new_file_path, index=False)

            print(f"Archivo procesado y guardado: {new_file_path}")
        except Exception as e:
            print(f"Ocurrió un error al procesar '{file_name}': {e}")

if __name__ == "__main__":
    #Revisa si el folder fue dado como argumento de línea
    if len(sys.argv) < 2:
        # Si no fue dado, pide input
        folder_path: str = input("Introduce la ruta al folder con los archivos CSV: ")
        folder_path = folder_path.strip('"').strip("'")
    else:
        #Usa el argumento de línea como ruta del folder de entrada
        folder_path = sys.argv[1].strip()
    # Call the function to delete the first row and save the files in a new folder
    delete_first_row_and_save_new_folder(folder_path)