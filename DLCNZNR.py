# Crea un archivo sin la ultima columna y sin ceros y reemplaza numeros restantes por 1, nombra todo con sufijo '_DLCNZNR'
#Idealmente este es el paso 1 & 2 & 3

import pandas as pd
import os
import sys
import csv


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
        new_file: str = os.path.join(new_folder_path, f"{file_name}_DLCNZNR{file_extension}")
        try:
            # Lee el CSV
            df = pd.read_csv(file_path)

            # Suelta la última columna
            df = df.iloc[:, :-1]

            # Guarda el DataFrame modificado a un nuevo archivo
            df.to_csv(new_file, index=False)

            # Intentamos quitar los ceros del archivo
            with open(new_file, mode='r', newline='') as infile:
                reader = csv.reader(infile)
                headers = next(reader)  # Read the header row

                filtered_rows = [headers]  # Start with the header row

                for row in reader:
                    # Check if all numeric values are zero
                    all_numeric_zero = True
                    for value in row:
                        try:
                            if float(value) != 0:
                                all_numeric_zero = False
                                break
                        except ValueError:
                            # Skip non-numeric values
                            continue

                    if not all_numeric_zero:
                        filtered_rows.append(row)

            with open(new_file, mode='w', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(filtered_rows)
            print(f"Todos los ceros y la última columna de {file} fueron borrados y procesados en {new_file}")

        except Exception as e:
            print(f"Error procesando {file}: {e}")

        # Registra cada CSV en un DataFrame de pandas
        df = pd.read_csv(new_file)

        # Loop through each column
        for column in df.columns:
            # Check if the column contains numeric data
            if pd.api.types.is_numeric_dtype(df[column]):
                # Replace numerical values with '1'
                df[column] = 1
            df.to_csv(new_file, index=False)

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
