import csv

input_file = 'tww-word_200646.csv'  # Replace with your input CSV file
output_file = 'tww-word.csv'  # Replace with your output CSV file

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        modified_row = [cell.replace('data/ocr/tww_word/', '', 1) if cell.startswith('data/ocr/tww_word/') else cell for cell in row]
        writer.writerow(modified_row)

