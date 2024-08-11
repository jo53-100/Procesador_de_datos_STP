#Este convierte archivos .xslx de una carpeta a .csv

import os
import sys
import pandas as pd


def excel_to_csv_folder(input_folder, output_folder_name):
    # Create output folder if it doesn't exist
    output_folder = os.path.join(input_folder, f'{output_folder_name}_csv')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the input folder
    files = os.listdir(input_folder)

    for file in files:
        if file.endswith('.xlsx'):
            excel_file = os.path.join(input_folder, file)
            csv_file = os.path.join(output_folder, file.replace('.xlsx', '.csv'))

            # Load the Excel file
            df = pd.read_excel(excel_file)

            # Save to CSV file
            df.to_csv(csv_file, index=False)

            print(f'Conversion successful: {excel_file} converted to {csv_file}')


if __name__ == "__main__":
    # Check if input folder path is provided as a command-line argument
    if len(sys.argv) < 2:
        # If not provided, ask for input interactively
        input_folder = input("Enter the path to the input folder containing Excel files: ").strip()
        input_folder = input_folder.strip('"').strip("'")
    else:
        # Use the provided command-line argument as input folder path
        input_folder = sys.argv[1].strip()

    # Specify the name for the output folder (e.g., 'output' will create 'output_csv')
    output_folder_name = 'output'

    excel_to_csv_folder(input_folder, output_folder_name)
