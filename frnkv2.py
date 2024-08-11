import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt


def plot_graphs(csv_file_path, save_plots=False):
    # Read data from CSV file
    df = pd.read_csv(csv_file_path)

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
    plt.bar(top_df.index, top_df['Percentage'], align='center', color='blue', alpha=0.7)
    plt.xlabel('Nombres de las dianas')
    plt.ylabel('Porcentaje')
    plt.title('Top 15 Dianas en términos de frecuencia')
    plt.xticks(top_df.index, top_df.iloc[:, 1], rotation=45)
    plt.grid(True)

    if save_plots:
        plt.savefig(os.path.splitext(csv_file_path)[0] + '_top15.png')
        print(f"Gráfico 'Top 15 Dianas' guardado como {os.path.splitext(csv_file_path)[0] + '_top15.png'}")
    else:
        plt.show()

    # Plotting 50+1
    plt.figure(figsize=(25, 18))  # Adjust figure size as needed
    filtered_df = df[df['Percentage'] > (df['Percentage'].max() / 2)]
    plt.bar(filtered_df.index, filtered_df['Percentage'], align='center', color='blue', alpha=0.7)
    plt.xlabel('Nombre común')
    plt.ylabel('Porcentaje')
    plt.title('Gráfica 50+1')
    plt.xticks(filtered_df.index, filtered_df.iloc[:, 1], rotation=45)
    plt.grid(True)

    if save_plots:
        plt.savefig(os.path.splitext(csv_file_path)[0] + '_50+1.png')
        print(f"Gráfico 'Gráfica 50+1' guardado como {os.path.splitext(csv_file_path)[0] + '_50+1.png'}")
    else:
        plt.show()


def process_file(file_path, new_folder_path):
    try:
        # Read CSV file
        df = pd.read_csv(file_path)

        # Drop the last column
        df = df.iloc[:, :-1]

        # Remove rows containing zeros
        df = df[(df != 0).all(axis=1)]

        # If DataFrame is not empty, process and save it
        if not df.empty:
            # Replace all remaining numbers with 1
            df[df.select_dtypes(include=[np.number]).columns] = 1

            # Construct the new file path
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))
            new_file_path = os.path.join(new_folder_path, f"{file_name}_processed{file_extension}")

            # Save the modified DataFrame to a new file
            df.to_csv(new_file_path, index=False)

            print(f"El archivo {file_name} fue procesado y guardado como {new_file_path}")
            return new_file_path

    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return None


def process_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"{folder_path} no es un directorio válido.")
        return

    # Create new folder name
    folder_name = os.path.basename(folder_path.rstrip('/'))
    new_folder_path = os.path.join(os.path.dirname(folder_path), f"{folder_name}_DLCNZN1")

    # Create new folder if it doesn't exist
    os.makedirs(new_folder_path, exist_ok=True)

    # List all CSV files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not files:
        print("No hay archivos CSV en el folder especificado.")
        return

    # Process each file
    processed_files = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        processed_file = process_file(file_path, new_folder_path)
        if processed_file:
            processed_files.append(processed_file)

    # Process the combined CSV files
    if processed_files:
        combined_output_file = os.path.join(os.path.dirname(new_folder_path), f"{folder_name}_combined.csv")
        process_csv_files(new_folder_path, combined_output_file)


def process_csv_files(new_folder_path, output_file):
    combined_data = pd.DataFrame()

    for filename in os.listdir(new_folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(new_folder_path, filename)

            # Extract the base name without suffixes
            column_name = os.path.splitext(filename)[0].split('_')[0]

            # Read the CSV file
            df = pd.read_csv(file_path)

            # Rename numeric columns
            numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
            df.rename(columns={col: column_name for col in numerical_columns}, inplace=True)

            # Append to combined data
            combined_data = pd.concat([combined_data, df], ignore_index=True)

    # Drop empty columns
    combined_data.dropna(axis=1, how='all', inplace=True)

    # Combine rows by 'Common name' and aggregate data
    combined_data = combined_data.groupby('Common name').agg(
        lambda x: ' '.join(x.dropna().unique()) if x.dtype == 'object' else x.sum()
    ).reset_index()

    # Write to output file
    combined_data.to_csv(output_file, index=False)
    print(f"Datos combinados guardados en {output_file}")

    # Generate plots
    plot_graphs(output_file)

    # Prompt user to save plots
    save_plots = input("¿Desea guardar las gráficas (s/n)? ").strip().lower()
    if save_plots == 's':
        plot_graphs(output_file, save_plots=True)


if __name__ == "__main__":
    # Check if input folder is provided as a command-line argument
    if len(sys.argv) < 2:
        # Prompt for input if not provided
        folder_path = input("Introduce la ruta al folder con los archivos CSV: ").strip().strip('"').strip("'")
    else:
        # Use the command-line argument as the input folder path
        folder_path = sys.argv[1].strip().strip('"').strip("'")

    # Process the folder
    process_folder(folder_path)
