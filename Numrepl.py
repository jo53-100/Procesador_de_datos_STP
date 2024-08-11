#Este cambia los numeros de un archivo y los reemplaza por '1', los cambios los guarda en un archivo nombrado _clean
import pandas as pd
import os
import sys


def replace_numerical_with_1(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Loop through each column
    for column in df.columns:
        # Check if the column contains numeric data
        if pd.api.types.is_numeric_dtype(df[column]):
            # Replace numerical values with '1'
            df[column] = 1

    # Prepare output file name
    output_file = os.path.splitext(csv_file)[0] + '_clean.csv'

    # Write the modified DataFrame back to the new CSV file
    df.to_csv(output_file, index=False)
    print(f'Modified data saved to {output_file}')


if __name__ == '__main__':
    # Check if the user provided a file path argument
    if len(sys.argv) < 2:
        print('Please provide the path to the CSV file as an argument.')
        sys.exit(1)

    # Extract the file path argument from command line
    csv_file = sys.argv[1]

    # Check if the file exists
    if not os.path.isfile(csv_file):
        print(f'Error: File not found at {csv_file}')
    else:
        # Call the function to process the CSV file
        replace_numerical_with_1(csv_file)
