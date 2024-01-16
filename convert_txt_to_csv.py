input_file = '/Users/marufahmed/Downloads/2023-stations.txt'  # Replace with your file name
output_file = '/Users/marufahmed/Downloads/2023-stations.csv'    # Name for the output CSV file

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # Split the line based on spaces or tabs
        data = line.split()
        # Join the split data with commas to create a CSV line
        csv_line = ','.join(data)
        outfile.write(csv_line + '\n')

