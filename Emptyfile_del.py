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
        print(f"Error reading {filepath}: {e}")
        return False


if __name__ == "__main__":
    # Get folder path from command line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/your/original_folder")
        sys.exit(1)

    original_folder = sys.argv[1]

    # Check if the provided path is a directory
    if not os.path.isdir(original_folder):
        print(f"Error: {original_folder} is not a valid directory.")
        sys.exit(1)

    # New folder path for files with numerical values
    new_folder = os.path.join(os.path.dirname(original_folder), os.path.basename(original_folder) + '_numerical')

    # Create the new folder if it doesn't exist
    os.makedirs(new_folder, exist_ok=True)

    # List all files in the original folder
    files = os.listdir(original_folder)

    # Filter .csv files with numerical values and copy them to new folder
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(original_folder, file)
            if contains_numerical_values(file_path):
                try:
                    # Copy the file to the new folder
                    shutil.copy(file_path, os.path.join(new_folder, file))
                    print(f"Copied {file} to {new_folder}")
                except Exception as e:
                    print(f"Error copying {file}: {e}")

    print(f"Files with numerical values have been copied to {new_folder}.")
