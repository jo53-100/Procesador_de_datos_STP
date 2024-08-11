import pandas as pd
import os
import sys


def delete_last_column(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Drop the last column
        df = df.iloc[:, :-1]

        # Save the modified DataFrame back to the same file
        df.to_csv(file_path, index=False)
        print(f"Successfully deleted the last column of {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_last_column.py <file1> <file2> ... <fileN>")
        sys.exit(1)

    files = sys.argv[1:]
    for file_path in files:
        if os.path.isfile(file_path):
            delete_last_column(file_path)
        else:
            print(f"{file_path} is not a valid file.")


if __name__ == "__main__":
    main()
