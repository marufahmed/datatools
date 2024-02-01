import os
import shutil
import pandas as pd

# Function to read CSV file with different delimiters
def read_csv_file(file_path):
    try:
        # Try reading with comma delimiter
        df = pd.read_csv(file_path, delimiter=',')
    except pd.errors.ParserError:
        # Handle the case if the file cannot be parsed
        raise ValueError("Error reading CSV file.")

    return df

# Read CSV file
csv_file_path = '/Users/marufahmed/Work/Machine Learning/RSNA/rsna_data_finalized_cleaned/train.csv'
df = read_csv_file(csv_file_path)

# Check if required columns exist
required_columns = ['patient_id', 'any_injury']
if not all(column in df.columns for column in required_columns):
    raise ValueError("Required columns not found in the CSV file.")

# Get the first column as patient_id
patient_id_col = df.columns[0]

# Path to the folder containing images
image_folder_path = '/Users/marufahmed/Work/Machine Learning/RSNA/rsna_data_finalized_cleaned'

# Output folders
output_folder_any_injury_0 = '/Users/marufahmed/Work/Machine Learning/RSNA/rsna_data_finalized_cleaned/any_injury_0/'
output_folder_any_injury_1 = '/Users/marufahmed/Work/Machine Learning/RSNA/rsna_data_finalized_cleaned/any_injury_1/'

## Iterate through each row in the CSV
for index, row in df.iterrows():
    patient_id = str(row[patient_id_col])
    any_injury = row['any_injury']
    
    # Find images with matching patient_id
    matching_images = [file for file in os.listdir(image_folder_path) if file.startswith(patient_id)]

    # Move images to appropriate folders based on any_injury value
    for image in matching_images:
        source_path = os.path.join(image_folder_path, image)
        if any_injury == 0:
            destination_path = os.path.join(output_folder_any_injury_0, image)
        else:
            destination_path = os.path.join(output_folder_any_injury_1, image)
        
        shutil.move(source_path, destination_path)

print("Image movement completed.")
