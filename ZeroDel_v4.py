#Este es el q hace un folder despues de borrar todos los ceros de cada archivo, los archivos y el folder nuevo los renombra con el sufijo '_sc'
#Paso 2
import csv
import os
import shutil


def remove_zero_rows(input_file, output_file):
    try:
        with open(input_file, mode='r', newline='') as infile:
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

        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(filtered_rows)

        print(f"Datos filtrados copiados a {output_file}")

    except FileNotFoundError:
        print(f"Archivo {input_file} no encontrado.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


def process_directory(input_dir):
    try:
        # Ensure the input directory exists
        if not os.path.isdir(input_dir):
            print(f"El directorio {input_dir} no existe.")
            return

        # Create the output directory
        base_name = os.path.basename(input_dir.rstrip(os.sep))
        parent_dir = os.path.dirname(input_dir.rstrip(os.sep))
        output_dir = os.path.join(parent_dir, f"{base_name}_sc")

        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        # Process each CSV file in the input directory
        for filename in os.listdir(input_dir):
            if filename.endswith('.csv'):
                input_file = os.path.join(input_dir, filename)
                file_base_name, file_extension = os.path.splitext(filename)
                output_file = os.path.join(output_dir, f"{file_base_name}_sc{file_extension}")
                remove_zero_rows(input_file, output_file)

        print(f"Todos los archivos CSV han sido procesados y guardados en {output_dir}")

    except Exception as e:
        print(f"Ha ocurrido un error al procesar el directorio: {e}")


if __name__ == "__main__":
    input_dir = input("Por favor entra la ruta al directorio que contiene los archivos CSV: ")
    input_dir = input_dir.strip('"').strip("'")
    process_directory(input_dir)
