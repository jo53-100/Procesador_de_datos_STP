#Este hace una grafica del top 15

import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(file_path):
    # Read data from CSV file
    df = pd.read_csv(file_path)

    # Extract text columns (first 5 columns assumed as text)
    text_columns = df.columns[:5]

    # Calculate the sum of each row for numerical columns
    df['RowSum'] = df.iloc[:, 5:].sum(axis=1)

    # Calculate the number of numeric columns
    num_numeric_columns = len(df.columns) - 5

    # Calculate the percentage for each row
    df['Percentage'] = (df['RowSum'] / num_numeric_columns) * 100

    # Sort the DataFrame by Percentage in descending order and select top 15 rows
    top_df = df.sort_values(by='Percentage', ascending=False).head(15)

    # Plotting
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed

    # Create bar positions
    bar_positions = range(len(top_df))

    # Plot bars
    plt.bar(bar_positions, top_df['Percentage'], align='center', color='blue', alpha=0.7)

    # Set labels and title
    plt.xlabel('Nombres de las dianas')
    plt.ylabel('Porcentaje')
    plt.title('Top 15 Dianas en terminos de frecuencia')

    # Set x-axis labels to text columns, only showing the first 8 characters
    plt.xticks(bar_positions, top_df.iloc[:, 1], rotation=45)

    # Show plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Ask for file path if not provided as command-line argument
        file_path = input("Enter the path to the CSV file: ").strip()
        file_path = file_path.strip('"').strip("'")
    else:
        file_path = sys.argv[1]
        file_path = file_path.strip('"').strip("'")
    plot_data(file_path)
