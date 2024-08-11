#Este hace lo mismo q la version pasada pero con un folder entero, los cambios los guarda en folder con sufijo _clean
#Este cambia los numeros de un de los archivos en un folder y los reemplaza por '1', los cambios los guarda en un folder con sufijo _clean
#Paso 4

import pandas as pd
import os
import sys


def replace_numerical_with_1(csv_file, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Loop through each column
    for column in df.columns:
        # Check if the column contains numeric data
        if pd.api.types.is_numeric_dtype(df[column]):
            # Replace numerical values with '1'
            df[column] = 1

    # Prepare output file name
    output_file = os.path.join(output_folder, os.path.basename(csv_file))

    # Write the modified DataFrame back to the new CSV file
    df.to_csv(output_file, index=False)
    print(f'Modified data saved to {output_file}')


if __name__ == '__main__':
    # Check if the user provided a folder path argument
    if len(sys.argv) < 2:
        print('Please provide the path to the folder containing CSV files as an argument.')
        sys.exit(1)

    # Extract the folder path argument from command line
    folder_path = sys.argv[1]

    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f'Error: Folder not found at {folder_path}')
        sys.exit(1)

    # Create output folder name
    output_folder = folder_path.rstrip(os.path.sep) + '_clean'

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Process each CSV file
    for csv_file in csv_files:
        csv_file_path = os.path.join(folder_path, csv_file)
        replace_numerical_with_1(csv_file_path, output_folder)

    print(f'Processing complete. Modified files saved in {output_folder}')
