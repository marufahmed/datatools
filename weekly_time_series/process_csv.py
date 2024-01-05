import csv

# Open the input text file and the output CSV file
with open('data_wunderground.txt', 'r') as infile, open('output.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Date', 'Time', 'Temperature (°F)', 'Dew Point (°F)', 'Humidity (%)', 'Wind Speed (mph)', 'Pressure (in)', 'Precipitation (in)'])

    # Read lines from the input file
    lines = infile.readlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() == 'Time':  # Check for the start of a new set of records
            # Extract the month and days
            month = lines[index + 1].strip()
            days = lines[index + 2].split()
            
            for day in days:
                # Write the data for each day with the corresponding date
                date = f"{month} {day}"
                time_data = lines[index + 5].split('\t')
                max_data = lines[index + 6].split('\t')
                avg_data = lines[index + 7].split('\t')
                min_data = lines[index + 8].split('\t')
                total_data = lines[index + 10].split('\t')
                for i in range(len(time_data)):
                    writer.writerow([date, time_data[i], max_data[i], avg_data[i], min_data[i], total_data[i]])

            index += 7  # Move the index to the next set of records

print("CSV file has been created successfully.")
