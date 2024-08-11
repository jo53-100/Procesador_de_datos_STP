#Hace un folder nuevo con puros archivos con numeros y los nombra _del
# Paso 4
import os
import shutil
import pandas as pd
import sys


# Function to check if a file contains numerical values
def contains_numerical_values(filepath):
    try:
        df = pd.read_csv(filepath)
        # Check if there are any numerical values in the dataframe
        return df.select_dtypes(include=['number']).shape[1] > 0
    except Exception as e:
        print(f"Error leyendo {filepath}: {e}")
        return False


if __name__ == "__main__":
    # Get folder path from command line argument
    if len(sys.argv) < 2:
        # Si no fue dado pide input
        folder = input("Introduce la ruta al folder con los archivos CSV: ").strip()
        folder = folder.strip('"').strip("'")
    else:
        # Usa el argumento de línea como ruta del folder de entrada
        folder = sys.argv[1].strip()


    # Check if the provided path is a directory
    if not os.path.isdir(folder):
        print(f"Error: {folder} No es un directorio válido.")
        sys.exit(1)

    # New folder path for files with numerical values
    Nuevo_folder = os.path.join(os.path.dirname(folder), os.path.basename(folder) + '_del')

    # Create the new folder if it doesn't exist
    os.makedirs(Nuevo_folder, exist_ok=True)

    # List all files in the original folder
    files = os.listdir(folder)

    # Filter .csv files with numerical values and copy them to new folder
    file: str
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(folder, file)
            if contains_numerical_values(file_path):
                try:
                    # Copy the file to the new folder
                    shutil.copy(file_path, os.path.join(Nuevo_folder, file))
                    print(f"{file} copiado a {Nuevo_folder}")

                    # Rename the copied file to have '_del' appended to its name
                    new_file_name = os.path.splitext(file)[0] + '_del' + os.path.splitext(file)[1]
                    os.rename(os.path.join(Nuevo_folder, file), os.path.join(Nuevo_folder, new_file_name))
                    print(f"{file} renombrado a {new_file_name}")
                except Exception as e:
                    print(f"Error procesando {file}: {e}")

    print(f"Los archivos con valores no nulos se han copiado en {Nuevo_folder}.")
