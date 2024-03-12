import os
import pandas as pd

# Function to count unique entries and their occurrences
def count_unique_entries(csv_file):
    data = pd.read_csv(csv_file)
    unique_values = data['chars_supervisor'].value_counts().reset_index()
    unique_values.columns = ['Character', 'Occurrences']
    return unique_values

# Directory containing CSV files
directory = '/Users/marufahmed/Work/Apurba/ocr_dataset_evaluation/statistics/new_statistics/content/char/separated_char_grapheme'

# Loop through each CSV file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        # Create filename for statistics CSV
        stats_filename = os.path.splitext(filename)[0] + '_statistics.csv'
        # Get unique entries and their occurrences
        unique_values = count_unique_entries(filepath)
        # Write statistics to CSV
        unique_values.to_csv(os.path.join(directory, stats_filename), index=False, encoding='utf-8-sig')

print("Statistics files have been created for each CSV file in the directory.")
