import os
import shutil

# Define the source folder where your .jpg files are located.
source_folder = '/Users/marufahmed/Work/Machine Learning/Datasets/ssc_test_questions/mcq'

# Define the subfolder where you want to move the renamed files.
subfolder = '/Users/marufahmed/Work/Machine Learning/Datasets/ssc_test_questions/mcq/extracted_images'

# Ensure the subfolder exists
os.makedirs(subfolder, exist_ok=True)

# List all the .jpg files in the source folder
jpg_files = [f for f in os.listdir(source_folder) if f.endswith('.jpg')]

for file_name in jpg_files:
    try:
        # Extract x and y from the file name
        x, y = map(int, os.path.splitext(file_name)[0].split('-'))

        # Calculate the new name as x + y
        new_name = f'{x + y}.jpg'

        # Construct the full paths for source and destination
        source_path = os.path.join(source_folder, file_name)
        dest_path = os.path.join(subfolder, new_name)

        # Rename and move the file
        shutil.move(source_path, dest_path)

        print(f'Renamed and moved: {file_name} -> {new_name}')

    except ValueError:
        print(f'Skipped: {file_name} (Invalid format)')

print('Renaming and moving complete.')
