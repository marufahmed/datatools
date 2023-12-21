import os
import cv2
import csv
from borno.word_recognition.base_word_ocr import BaseWordOCR

# Initialize OCR model
ocr_model = BaseWordOCR(model_type='computer', triton_config={})  # Update triton_config if required

# Directory path containing images
directory_path = '/home/apurba/DATASET/data/ocr/ccw_word/'

# Path to save CSV file
csv_file_path = './evaluation/ccw_word.csv'

# Path to save exceptions CSV file
exceptions_csv_file_path = './evaluation/exceptions.csv'

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
with open(csv_file_path, 'a', newline='') as csvfile, open(exceptions_csv_file_path, 'a', newline='') as exceptions_csvfile:
    fieldnames = ['ID', 'Text']
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
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)  # Read as grayscale

            # Perform OCR
            ocr_result = ocr_model.infer({"images": [{"id": filename, "name": image}]})

            # Print OCR detection
            print(f"OCR Detection for {filename}:")
            for result in ocr_result:
                print(f"ID: {result['id']}, Text: {result['text']}")
                # Write to CSV file
                writer.writerow({'ID': result['id'], 'Text': result['text']})

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

