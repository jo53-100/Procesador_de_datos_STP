import csv
import os


def remove_zero_rows(input_file):
    try:
        # Remove any surrounding quotes from the input file path
        input_file = input_file.strip('"').strip("'")

        # Extract the base name and extension from the input file
        base_name, extension = os.path.splitext(input_file)
        # Create the output file name by appending '_py' to the base name
        output_file = f"{base_name}_py{extension}"

        with open(input_file, mode='r', newline='') as infile:
            reader = csv.reader(infile)
            headers = next(reader)  # Read the header row

            filtered_rows = [headers]  # Start with the header row

            for row in reader:
                # Check if all numerical values are not zero
                all_values_non_zero = True
                for value in row:
                    try:
                        if float(value) == 0:
                            all_values_non_zero = False
                            break
                    except ValueError:
                        # Skip non-numeric values
                        continue

                if all_values_non_zero:
                    filtered_rows.append(row)

        with open(output_file, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(filtered_rows)

        print(f"Filtered data saved to {output_file}")

    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    input_csv = input("Please enter the full path to the CSV file: ")
    remove_zero_rows(input_csv)
