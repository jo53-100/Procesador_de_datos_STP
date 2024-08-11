# Este convierte archivos .xslx de una carpeta a .csv, además de eso borra la primera fila del archivo, así queda con el formato del paso 1 .y los guarda en una carpeta con sufijo '_csv'
# Idealmente este es el paso 0

import os
import sys
import pandas as pd


def excel_a_csv(folder_de_entrada, nombre_folder_nuevo):
    # Revisa si el folder existe
    if not os.path.isdir(folder_de_entrada):
        print(f"El folder '{folder_de_entrada}' no existe.")
        return

    # Toma el nombre del folder de entrada y crea un nuevo folder con el sufijo '_csv'.
    nombre_folder = os.path.basename(folder_de_entrada.rstrip('/'))
    ruta_folder_nuevo = os.path.join(os.path.dirname(folder_de_entrada), nombre_folder_nuevo)

    # Crea el folder si no existe
    os.makedirs(ruta_folder_nuevo, exist_ok=True)

    # Lista todos los archivos en el folder de entrada
    files = os.listdir(folder_de_entrada)

    for file in files:
        if file.endswith('.xlsx'):
            excel_file = os.path.join(folder_de_entrada, file)
            csv_file = os.path.join(ruta_folder_nuevo, file.replace('.xlsx', '.csv'))

            # Carga el archivo de Excel
            df = pd.read_excel(excel_file)

            # Guarda a archivo CSV
            df = df.to_csv(csv_file, index=False)
            df = pd.read_csv(csv_file, skiprows=1)
            df = df.to_csv(csv_file, index=False)

            print(f'Conversión exitosa: {excel_file} convertido a {csv_file}')


if __name__ == "__main__":
    # Revisa si el folder de entrada es dado como argumento de línea
    if len(sys.argv) < 2:
        # Si no fue dado, pide input
        folder_de_entrada = input("Introduce la ruta al folder con los archivos .xlsx: ").strip()
        folder_de_entrada = folder_de_entrada.strip('"').strip("'")
        Nombre_folder_nuevo = os.path.basename(folder_de_entrada.rstrip('/')) + "_csv"
    else:
        # Usa el argumento de línea como ruta del folder de entrada
        folder_de_entrada = sys.argv[1].strip()
        Nombre_folder_nuevo = os.path.basename(folder_de_entrada.rstrip('/')) + "_csv"
    # llama la primera función
    excel_a_csv(folder_de_entrada, Nombre_folder_nuevo)