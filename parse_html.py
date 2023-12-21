from bs4 import BeautifulSoup
import pandas as pd

# Read HTML content from file
with open('to_extract_current.html', 'r') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

data = []

# Finding all the conference items
conference_items = soup.find_all(class_='conference-item')

for conference in conference_items:
    rank = conference.find(class_='position').get_text(strip=True)
    conference_name = conference.find('h4').get_text(strip=True)
    
    # Extracting Dates & Location separately
    info_div = conference.find(class_='info')
    date_range = ' - '.join([date.text.strip() for date in info_div.find_all('span') if date.text.strip()])
    
    # Check if a strong tag exists within the info_div
    location_tag = info_div.find('strong')
    location = location_tag.text.strip() if location_tag else 'Location not available'
    
    ranking = conference.find(class_='ranking').get_text(strip=True)
    data.append([rank, conference_name, date_range, location, ranking])

# Create a DataFrame and save to CSV
df = pd.DataFrame(data, columns=['Rank', 'Conference Name', 'Dates', 'Location', 'Ranking'])
df.to_csv('conference_data_current.csv', index=False)

