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
with open(csv_file_path, 'a', newline='') as csvfile:
    fieldnames = ['ID', 'Text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header only if the file is empty
    if os.stat(csv_file_path).st_size == 0:
        writer.writeheader()

    # Traverse through the directory
    for filename in os.listdir(directory_path):
        if last_processed_image is not None:
            if filename == last_processed_image:
                last_processed_image = None  # Start processing from the next image
            continue

        if filename.endswith((".jpg", ".png")):  # Add other image extensions if needed
            file_path = os.path.join(directory_path, filename)
            
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

# Inform user about CSV file creation
print(f"OCR results are saved in '{csv_file_path}'")
