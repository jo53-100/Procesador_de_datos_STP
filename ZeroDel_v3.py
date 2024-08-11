#Este es el q hace los folders

import csv
import os
import shutil


def remove_zero_rows(input_file, output_file):
    try:
        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            headers = next(reader)  # Read the header row

            filtered_rows = [headers]  # Start with the header row

            for row in reader:
                # Check if all numeric values are zero
                all_numeric_zero = True
                for value in row:
                    try:
                        if float(value) != 0:
                            all_numeric_zero = False
                            break
                    except ValueError:
                        # Skip non-numeric values
                        continue

                if not all_numeric_zero:
                    filtered_rows.append(row)

        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(filtered_rows)

        print(f"Filtered data saved to {output_file}")

    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_directory(input_dir):
    try:
        # Ensure the input directory exists
        if not os.path.isdir(input_dir):
            print(f"The directory {input_dir} does not exist.")
            return

        # Create the output directory
        base_name = os.path.basename(input_dir.rstrip(os.sep))
        parent_dir = os.path.dirname(input_dir.rstrip(os.sep))
        output_dir = os.path.join(parent_dir, f"{base_name}_py")

        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        # Process each CSV file in the input directory
        for filename in os.listdir(input_dir):
            if filename.endswith('.csv'):
                input_file = os.path.join(input_dir, filename)
                output_file = os.path.join(output_dir, filename)
                remove_zero_rows(input_file, output_file)

        print(f"All CSV files have been processed and saved to {output_dir}")

    except Exception as e:
        print(f"An error occurred while processing the directory: {e}")


if __name__ == "__main__":
    input_dir = input("Please enter the full path to the directory containing the CSV files: ")
    input_dir = input_dir.strip('"').strip("'")
    process_directory(input_dir)