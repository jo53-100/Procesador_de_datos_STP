#Borra la primera fila, este script se usa cuando tuviste que convertir el archivo de .xslx a .csv
#Guarda los archivos procesados con el sufijo '_FRD'
#Idealmente este es el paso 0.5

import os
import pandas as pd

def delete_first_row_and_save_new_folder(folder_path):
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # Get the name of the input folder and create a new folder with '_FDR' suffix
    folder_name = os.path.basename(folder_path.rstrip('/'))
    new_folder_name = f"{folder_name}_FRD"
    new_folder_path = os.path.join(os.path.dirname(folder_path), new_folder_name)

    # Create the new folder if it doesn't exist
    os.makedirs(new_folder_path, exist_ok=True)

    # Get a list of all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Loop through each CSV file
    for file_name in csv_files:
        original_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(new_folder_path, file_name)

        try:
            # Read the CSV file, skipping the first row
            df = pd.read_csv(original_file_path, skiprows=1)

            # Save the DataFrame to the new folder
            df.to_csv(new_file_path, index=False)

            print(f"Processed and saved file: {new_file_path}")
        except Exception as e:
            print(f"An error occurred while processing '{file_name}': {e}")

if __name__ == "__main__":
    # Prompt the user to input the folder path
    folder_path = input("Please enter the path to the folder containing the CSV files: ")
    folder_path = folder_path.strip('"').strip("'")
    # Call the function to delete the first row and save the files in a new folder
    delete_first_row_and_save_new_folder(folder_path)
