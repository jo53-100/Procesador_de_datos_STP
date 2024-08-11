#Este borra la ultima columna de un folder, usar solo una vez lol

import pandas as pd
import os
import sys


def delete_last_column(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Drop the last column
        df = df.iloc[:, :-1]

        # Save the modified DataFrame back to the same file
        df.to_csv(file_path, index=False)
        print(f"Última columna de {file_path} fue borrada exitosamente")
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")


def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} no es un directorio válido.")
        return

    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not files:
        print("No hay archivos CSV en el folder especificado.")
        return

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        delete_last_column(file_path)


def main():
    if len(sys.argv) != 2:
        print("Uso: DLCv2.py <ruta_del_folder>")
        sys.exit(1)

    folder_path = sys.argv[1]
    process_folder(folder_path)


if __name__ == "__main__":
    main()
