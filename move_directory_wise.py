import os
import shutil

# Function to create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to move files to the appropriate directories
def move_files(source_dir, destination_dir, filenames):
    for filename in filenames:
        shutil.move(os.path.join(source_dir, filename), destination_dir)

# Function to organize files
def organize_files(source_dir):
    for filename in os.listdir(source_dir):
        if filename.endswith('.png'):
            parts = filename.split('_')
            patient_name = parts[0]
            scan_id = '_'.join(parts[0:2])

            # Create patient directory if it doesn't exist
            patient_dir = os.path.join(source_dir, patient_name)
            create_directory(patient_dir)

            # Create scan directory if it doesn't exist
            scan_dir = os.path.join(patient_dir, scan_id)
            create_directory(scan_dir)

            # Move file to the scan directory
            move_files(source_dir, scan_dir, [filename])

# Provide the path to your folder containing the CT scan images
source_directory = "/archive"

# Organize the files
organize_files(source_directory)
