import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

base_url = 'https://www.wunderground.com/history/daily/us/tx/austin/KAUS/date/'
start_date = datetime(2023, 12, 1)
end_date = datetime(2023, 12, 31)

# Create a CSV file
with open('december_weather.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Loop through each day in December
    current_date = start_date
    while current_date <= end_date:
        # Generate the URL for the current date
        formatted_date = current_date.strftime('%Y-%m-%d')
        url = base_url + formatted_date

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all tables within the page
            tables = soup.find_all('table')

            # Loop through each table
            for table in tables:
                # Extract table rows
                rows = table.find_all('tr')
                for row in rows:
                    # Extract data cells
                    data = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
                    # Write data to CSV
                    writer.writerow(data)
                # Add an empty row as a separator between tables
                writer.writerow([])

        else:
            print(f'Failed to retrieve data for {formatted_date}')

        # Move to the next day
        current_date += timedelta(days=1)
