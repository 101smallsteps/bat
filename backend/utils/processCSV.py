import csv
import sys


def remove_spaces(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            # Remove spaces from each field in the row
            modified_row = [field.replace(' ', '') for field in row]
            # Write the modified row to the output CSV file
            writer.writerow(modified_row)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    remove_spaces(input_file, output_file)
