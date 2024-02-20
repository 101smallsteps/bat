import pandas as pd
import sys
def print_first_column(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Print the first column
    first_column = df.iloc[:, 0]

    first_column.to_csv(output_file,index=False, header=False)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    print_first_column(input_file, output_file)
