#este hace un grafico de todos los datos

import sys
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(file_path):
    # Read data from CSV file
    df = pd.read_csv(file_path)

    # Extract text columns (first 5 columns assumed as text)
    text_columns = df.columns[:5]

    # Compute row sums
    df['RowSum'] = df.iloc[:, 5:].sum(axis=1)

    # Plotting
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed

    # Plot bars
    plt.bar(df.index, df['RowSum'], align='center', color='blue', alpha=0.7)

    # Set labels and title
    plt.xlabel('Row Names')
    plt.ylabel('Sum of Values')
    plt.title('Sum of Row Values')

    # Set x-axis labels to text columns
    plt.xticks(df.index, df[text_columns].apply(lambda row: ', '.join(row), axis=1), rotation=45)

    # Show plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Ask for file path if not provided as command-line argument
        file_path = input("Enter the path to the CSV file: ").strip()
    else:
        file_path = sys.argv[1]

    plot_data(file_path)
