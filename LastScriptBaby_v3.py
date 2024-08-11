#Este ya hace un archivo .csv limpio y ordenado, no grafica, une filas considerando que se llamen igual en la primera columna

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

    # Combine rows with the same text cells (assumes the first column is the text column)
    combined_data = combined_data.groupby(combined_data.columns[1]).agg(lambda x: ' '.join(x.unique()) if x.dtype == 'object' else x.sum()).reset_index()

    # Output file path in the same directory as input folder
    output_folder = os.path.dirname(folder_path)
    output_file_path = os.path.join(output_folder, 'Clean Data.csv')

    # Write to output file
    combined_data.to_csv(output_file_path, index=False)
    print(f"Combined data saved to {output_file_path}")

if __name__ == "__main__":
    # Prompt user to input folder path
    folder_path_input = input("Enter the folder path containing CSV files (use 'Copy as path' format): ").strip()

    # Remove surrounding double quotes if present
    if folder_path_input.startswith('"') and folder_path_input.endswith('"'):
        folder_path_input = folder_path_input[1:-1]

    # Replace double backslashes with single backslashes
    folder_path = folder_path_input.replace('\\\\', '\\')

    print(f"Entered folder path: {folder_path}")

    # Convert to absolute path
    folder_path = os.path.abspath(folder_path)

    # Verify if the folder path is valid
    if not os.path.isdir(folder_path):
        print(f"Error: The folder path '{folder_path}' is not valid or does not exist.")
    else:
        process_csv_files(folder_path, 'Clean Data.csv')
