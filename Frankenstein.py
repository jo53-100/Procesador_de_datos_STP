# Hace todo ya de one de volon pimpon soy buenisimooooooooo


import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt


def plot_graphs(output_file, save_plots=False):
    # Read data from CSV file
    df = pd.read_csv(output_file)

    # Calculate the sum of each row for numerical columns
    df['RowSum'] = df.iloc[:, 5:].sum(axis=1)

    # Calculate the number of numeric columns
    num_numeric_columns = len(df.columns) - 5

    # Calculate the percentage for each row
    df['Percentage'] = (df['RowSum'] / num_numeric_columns) * 100

    # Sort the DataFrame by Percentage in descending order and select top 15 rows
    top_df = df.sort_values(by='Percentage', ascending=False).head(15)

    # Plotting top 15 dianas
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    bar_positions_top = range(len(top_df))
    plt.bar(bar_positions_top, top_df['Percentage'], align='center', color='blue', alpha=0.7)
    plt.xlabel('Nombres de las dianas')
    plt.ylabel('Porcentaje')
    plt.title('Top 15 Dianas en términos de frecuencia')
    plt.xticks(bar_positions_top, top_df.iloc[:, 1], rotation=45)
    plt.grid(True)

    # Plotting 50+1
    plt.figure(figsize=(25, 18))  # Adjust figure size as needed
    filtered_df = df[df['Percentage'] > (df['Percentage'].max() / 2)]
    bar_positions_filtered = range(len(filtered_df))
    plt.bar(bar_positions_filtered, filtered_df['Percentage'], align='center', color='blue', alpha=0.7)
    plt.xlabel('Nombre común')
    plt.ylabel('Porcentaje')
    plt.title('Gráfica 50+1')
    plt.xticks(bar_positions_filtered, filtered_df.iloc[:, 1], rotation=45)
    plt.grid(True)

    # Save or show plots based on user input
    if save_plots:
        plt.savefig(os.path.splitext(output_file)[0] + '_top15.png')
        print(f"Gráfico 'Top 15 Dianas' guardado como {os.path.splitext(output_file)[0] + '_top15.png'}")
        plt.savefig(os.path.splitext(output_file)[0] + '_50+1.png')
        print(f"Gráfico 'Gráfica 50+1' guardado como {os.path.splitext(output_file)[0] + '_50+1.png'}")
    else:
        plt.show()


def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} no es un directorio válido.")
        return

    # Toma el nombre del folder y crea uno nuevo con el sufijo '_DLCNZN1'
    folder_name = os.path.basename(folder_path.rstrip('/'))
    new_folder_name = f"{folder_name}_processed"
    new_folder_path: str = os.path.join(os.path.dirname(folder_path), new_folder_name)

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
        new_file = os.path.join(new_folder_path, f"{file_name}_processed{file_extension}")

        try:
            # Lee el CSV
            df = pd.read_csv(file_path)

            # Suelta la última columna
            df = df.iloc[:, :-1]

            # Elimina filas que contienen ceros
            df = df[(df != 0).all(axis=1)]

            # Verifica si el DataFrame está vacío después de las operaciones
            if not df.empty:
                # Reemplaza todos los números restantes por 1
                df[df.select_dtypes(include=[np.number]).columns] = 1

                # Guarda el DataFrame modificado a un nuevo archivo
                df.to_csv(new_file, index=False)

                print(f"El archivo {file} fue procesado y guardado como {new_file}")

        except Exception as e:
            print(f"Error procesando {file}: {e}")

    # Procesa archivos CSV en la nueva carpeta
    process_csv_files(new_folder_path, output_file)


def process_csv_files(new_folder_path, output_file):
    combined_data = pd.DataFrame()

    # Itera sobre los archivos en la carpeta
    for filename in os.listdir(new_folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(new_folder_path, filename)

            # Extrae el nombre de la columna sin sufijos '_...'
            column_name = os.path.splitext(filename)[0].split('_')[0]

            # Lee el archivo CSV
            df = pd.read_csv(file_path)

            # Renombra columnas numéricas
            numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
            rename_mapping = {col: column_name for col in numerical_columns}
            df.rename(columns=rename_mapping, inplace=True)

            # Añade al combined_data
            combined_data = pd.concat([combined_data, df], ignore_index=True)

    # Elimina columnas vacías
    combined_data.dropna(axis=1, how='all', inplace=True)

    # Almacena el orden original de las columnas
    original_column_order = combined_data.columns

    # Combina filas basadas en 'Common name' y agrega datos
    combined_data = combined_data.groupby('Common name').agg(
        lambda x: ' '.join(x.dropna().unique()) if x.dtype == 'object' else x.sum()
    ).reset_index()

    # Reordena columnas para que coincidan con el orden original
    combined_data = combined_data[original_column_order]

    # Escribe en archivo de salida
    combined_data.to_csv(output_file, index=False)
    print(f"Datos combinados guardados en {output_file}")

    # Genera las gráficas
    plot_graphs(output_file)

    # Prompt user to save plots
    save_plots = input("¿Desea guardar las gráficas (s/n)? ").strip().lower()
    if save_plots == 's':
        plot_graphs(output_file, save_plots=True)


if __name__ == "__main__":
    # Revisa si el folder de entrada es dado como argumento de línea
    if len(sys.argv) < 2:
        # Si no fue dado pide input
        folder_path = input("Introduce la ruta al folder con los archivos CSV: ").strip().strip('"').strip("'")

    else:
        # Usa el argumento de línea como ruta del folder de entrada
        folder_path = sys.argv[1].strip().strip('"').strip("'")

    # Determina el directorio padre del folder especificado
    parent_directory = os.path.dirname(folder_path)
    output_file = os.path.join(parent_directory, f"{folder_path}.csv")

    # Llama la función para procesar el folder
    process_folder(folder_path)
