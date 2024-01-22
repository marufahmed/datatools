import os
import cv2
import csv
import time
import numpy as np
import logging

from borno.char_recognition.grapheme_recognition_v2 import GraphemeRecognition
from borno.char_recognition import char_seg_pixel, chars_postproc


# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Initialize OCR model
def get_char_model():
    start_time = time.time()

    # Initialize GraphemeRecognition without Triton
    char_recog_model = GraphemeRecognition(triton_config=None,triton=False)

    load_time = round(time.time() - start_time, 4)
    logger.info(f"Character model loading time: {load_time}")
    return char_recog_model

# Directory path containing images
directory_path = '/Users/marufahmed/Work/Apurba/OCR DATASET/data/ocr/ccw_word'

# Path to save CSV file
csv_file_path = '/Users/marufahmed/Work/Apurba/ocr_dataset_evaluation/prediction_char/ccw_word_characterModel.csv'

# Path to save exceptions CSV file
exceptions_csv_file_path = '/Users/marufahmed/Work/Apurba/ocr_dataset_evaluation/prediction_char/exceptions_ccw_word_characterModel.csv'


# Initialize OCR model
ocr_model = get_char_model()  # Get the model using the function

# Track progress
total_images = len([name for name in os.listdir(directory_path) if name.endswith((".jpg", ".png"))])
processed_count = 0

# Check if CSV file exists and find the last processed image
last_processed_image = None
if os.path.exists(csv_file_path):
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            last_processed_image = row['ID']
    print(f"Resuming OCR from image: {last_processed_image}")

# Open CSV file to write results (append mode)
with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile, open(exceptions_csv_file_path, 'a', newline='', encoding='utf-8-sig') as exceptions_csvfile:
    fieldnames = ['ID', 'Characters']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    exceptions_writer = csv.DictWriter(exceptions_csvfile, fieldnames=['ID', 'Exception'])

    # Write header only if the file is empty
    if os.stat(csv_file_path).st_size == 0:
        writer.writeheader()
    if os.stat(exceptions_csv_file_path).st_size == 0:
        exceptions_writer.writeheader()

    # Get a sorted list of filenames
    file_list = sorted([filename for filename in os.listdir(directory_path) if filename.endswith((".jpg", ".png"))])

    # Find the index of the last processed image
    if last_processed_image is not None:
        try:
            start_index = file_list.index(last_processed_image) + 1
            file_list = file_list[start_index:]  # Start from the next image
        except ValueError:
            pass  # Handle the case if the last processed image is not found in the directory

    # Process the sorted file list sequentially
    for filename in file_list:
        file_path = os.path.join(directory_path, filename)
        
        try:
            # Read the image using OpenCV
            image = cv2.imread(file_path)

            seg_img_dict = char_seg_pixel(image)
            seg_img = seg_img_dict['chars']
            ocr_result = ocr_model.predict_chars(seg_img)

            # Print OCR detection
            print(f"OCR Detection for {filename}: {ocr_result}")
            
            # Convert the list of characters to a word
            word = ''.join(ocr_result)

            # Write to CSV file
            writer.writerow({'ID': filename, 'Text': word, 'Characters': ocr_result})

            processed_count += 1
            # Update progress
            print(f"Processed {processed_count} out of {total_images} images")

        except Exception as e:
            # If an exception occurs, save details to exceptions.csv
            print(f"Error processing {filename}: {e}")
            exceptions_writer.writerow({'ID': filename, 'Exception': str(e)})
        
        

# Inform user about CSV file creation
print(f"OCR results are saved in '{csv_file_path}'")
print(f"Exceptions are saved in '{exceptions_csv_file_path}'")