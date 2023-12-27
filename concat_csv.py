import pandas as pd

# Paths to the original CSV files
file1_path = 'ground_truth_gold_standard/HandWritten/04_hwiw_word_to_page.csv'
file2_path = 'ground_truth_gold_standard/HandWritten/06_hwrw_word_to_page.csv'

# Columns to extract from each file
columns_to_extract_file1 = ['path', 'chars_supervisor']  # Replace with your column names from file 1
columns_to_extract_file2 = ['path', 'chars_supervisor']  # Replace with your column names from file 2

# Read specific columns from the CSV files
data_file1 = pd.read_csv(file1_path, usecols=columns_to_extract_file1)
data_file2 = pd.read_csv(file2_path, usecols=columns_to_extract_file2)

# Write the extracted data from the second file to the bottom of the first file
combined_data = pd.concat([data_file1, data_file2], ignore_index=True)

# Path for the new CSV file with combined columns
combined_file_path = 'ground_truth_gold_standard/hwrw_word.csv'

# Write the combined data to a new CSV file
combined_data.to_csv(combined_file_path, index=False, encoding='utf-8-sig')
