#Este hace lo mismo q la version pasada pero con un folder entero, los cambios los guarda en folder con sufijo _clean
#Este cambia los numeros de un de los archivos en un folder y los reemplaza por '1', los cambios los guarda en un folder con sufijo _clean
#Paso 3

import pandas as pd
import os
import sys


def replace_numerical_with_1(folder_path):
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f'Error: No se encontró ningún folder en {folder_path}')
        return

    # Toma el nombre del folder de entrada y crea uno nuevo con el sufijo '_clean'
    folder_name = os.path.basename(folder_path.rstrip('/'))
    new_folder_name = f"{folder_name}_clean"
    output_folder = os.path.join(os.path.dirname(folder_path), new_folder_name)


    # Crea el nuevo folder si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Toma todos los archivos CSV en el folder de entrada
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Procesa cada CSV
    for csv_file in csv_files:
        csv_file_path = os.path.join(folder_path, csv_file)

        # Registra cada CSV en un DataFrame de pandas
        df = pd.read_csv(csv_file_path)

        # Loop through each column
        for column in df.columns:
            # Check if the column contains numeric data
            if pd.api.types.is_numeric_dtype(df[column]):
                # Replace numerical values with '1'
                df[column] = 1

        # Prepare output file name
        output_file = os.path.join(output_folder, csv_file)


        # Write the modified DataFrame back to the new CSV file
        df.to_csv(output_file, index=False)
        print(f'Datos modificados guardados en {output_file}')


if __name__ == '__main__':
    # Revisa si el folder fue dado como argumento de línea
    if len(sys.argv) < 2:
        # Si no fue dado, pide input
        folder_path: str = input("Introduce la ruta al folder con los archivos CSV: ")
        folder_path = folder_path.strip('"').strip("'")
    else:
        # Usa el argumento de línea como ruta del folder de entrada
        folder_path = sys.argv[1].strip()

    #Llama la función
    replace_numerical_with_1(folder_path)

