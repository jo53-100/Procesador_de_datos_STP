#Este es el programa que hace las graficas, aqui se usa el folder ya limpio con los datos bien formateados, peinados y perfumados
#Este es la version 1, ya combina las celdas pero tiene todavia errores; combina las celdas no numericas y repite los nombresd que haya en ellas

import os
import pandas as pd

def process_csv_files(folder_path, output_file):
    combined_data = pd.DataFrame()

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # Extract column name without '_...' suffixes
            column_name = os.path.splitext(filename)[0].split('_')[0]

            # Read CSV file
            df = pd.read_csv(file_path)

            # Rename numerical columns
            numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
            rename_mapping = {col: column_name for col in numerical_columns}
            df.rename(columns=rename_mapping, inplace=True)

            # Append to combined_data
            combined_data = pd.concat([combined_data, df], ignore_index=True)

    # Group by rows with the same names and sum numerical values
    combined_data = combined_data.groupby(combined_data.columns[0]).sum().reset_index()

    # Write to output file
    combined_data.to_csv(output_file, index=False)
    print(f"Combined data saved to {output_file}")

if __name__ == "__main__":
    # Prompt user to input folder path
    folder_path = input("Enter the absolute folder path containing CSV files: ").strip()

    # Convert to absolute path
    folder_path = os.path.abspath(folder_path)

    print(f"Entered folder path: {folder_path}")

    # Verify if the folder path is valid
    if not os.path.isdir(folder_path):
        print(f"Error: The folder path '{folder_path}' is not valid or does not exist.")
    else:
        output_file = 'combined_data.csv'
        process_csv_files(folder_path, output_file)
