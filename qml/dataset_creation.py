# This script is used to move, rename , balance and split the entire dataset
import os
import shutil
import pandas as pd
import random

# Read train.csv file
csv_file_path = 'train.csv'
df = pd.read_csv(csv_file_path)

# Check if required columns exist
required_columns = ['patient_id', 'any_injury']
if not all(column in df.columns for column in required_columns):
    raise ValueError("Required columns not found in the CSV file.")

# Extract patient IDs from filenames and create mapping
patient_id_mapping = {}
image_folder_path = './combined_rgb'  # Assuming images are in the current directory
for filename in os.listdir(image_folder_path):
    if filename.endswith('.jpg'):
        parts = filename.split('-')
        patient_id = parts[0]
        patient_id_mapping[filename] = int(df[df['patient_id'] == int(patient_id)]['any_injury'])

# Define paths for the dataset
dataset_path = 'dataset'
train_path = os.path.join(dataset_path, 'Train')
val_path = os.path.join(dataset_path, 'Validation')
test_path = os.path.join(dataset_path, 'Test')

# Create directories for the dataset
for path in [train_path, val_path, test_path]:
    os.makedirs(os.path.join(path, 'Any_injury_0'), exist_ok=True)
    os.makedirs(os.path.join(path, 'Any_injury_1'), exist_ok=True)

# Class imbalance handling: Count occurrences of each class
class_counts = {0: 0, 1: 0}
for label in patient_id_mapping.values():
    class_counts[label] += 1

# Determine undersampling ratio
undersampling_ratio = min(class_counts.values()) / max(class_counts.values())

# Shuffle and split filenames into train, validation, and test sets
filenames = list(patient_id_mapping.keys())
random.shuffle(filenames)
train_size = int(0.6 * len(filenames))
val_size = int(0.2 * len(filenames))
test_size = int(0.2 * len(filenames))

train_filenames = filenames[:train_size]
val_filenames = filenames[train_size:train_size + val_size]
test_filenames = filenames[train_size + val_size:]

# Function to move images to appropriate folders and perform undersampling
def move_images(filenames, destination_path):
    for filename in filenames:
        label = patient_id_mapping[filename]
        source_path = os.path.join(image_folder_path, filename)
        if random.random() > undersampling_ratio and class_counts[label] > min(class_counts.values()):
            # Skip the image for undersampling
            continue
        shutil.copy(source_path, os.path.join(destination_path, f'Any_injury_{label}', filename))
        class_counts[label] -= 1

# Move images to train, validation, and test folders
move_images(train_filenames, train_path)
move_images(val_filenames, val_path)
move_images(test_filenames, test_path)

print("Dataset creation completed.")
