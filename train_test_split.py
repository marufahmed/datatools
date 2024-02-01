import os
import shutil
import random

def create_train_test_split(input_folder, output_folder, split_ratio=0.8):
    # Create train and test folders inside the output folder
    train_folder = os.path.join(output_folder, 'train')
    test_folder = os.path.join(output_folder, 'test')

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)

    # Get the list of image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]

    # Shuffle the list of image files
    random.shuffle(image_files)

    # Calculate the split index based on the split ratio
    split_index = int(len(image_files) * split_ratio)

    # Copy the images to the train folder
    for image_file in image_files[:split_index]:
        src_path = os.path.join(input_folder, image_file)
        dst_path = os.path.join(train_folder, image_file)
        shutil.copy(src_path, dst_path)

    # Copy the images to the test folder
    for image_file in image_files[split_index:]:
        src_path = os.path.join(input_folder, image_file)
        dst_path = os.path.join(test_folder, image_file)
        shutil.copy(src_path, dst_path)

# Specify the input and output folders for each class
input_folder_0 = '/Users/marufahmed/Work/Machine Learning/RSNA/rsna_data_finalized_cleaned/any_injury_0/'
output_folder_0 = '/Users/marufahmed/Work/Machine Learning/RSNA/rsna_data_finalized_cleaned/any_injury_0_split'

input_folder_1 = '/Users/marufahmed/Work/Machine Learning/RSNA/rsna_data_finalized_cleaned/any_injury_1/'
output_folder_1 = '/Users/marufahmed/Work/Machine Learning/RSNA/rsna_data_finalized_cleaned/any_injury_1_split'

# Create train-test split for each class
create_train_test_split(input_folder_0, output_folder_0)
create_train_test_split(input_folder_1, output_folder_1)
