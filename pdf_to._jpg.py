import os
import subprocess
from glob import glob

# Define an initial index
start_index = 0

# Specify the folder containing your PDF files
pdf_folder = "/Users/marufahmed/Work/Machine Learning/Datasets/ssc_test_questions/mcq"

# Use glob to get a list of PDF files
pdf_files = glob(os.path.join(pdf_folder, '*.pdf'))

# Loop through all PDF files in the folder
for pdf_file in pdf_files:
    # Use the `convert` command with the starting index
    subprocess.run(['convert', '-density', '300', pdf_file, f'{start_index}.jpg'])
    
    # Update the starting index for the next file
    pdf_info = subprocess.check_output(['pdfinfo', pdf_file]).decode()
    num_pages = int([line for line in pdf_info.split('\n') if line.startswith('Pages:')][0].split(': ')[1])
    start_index += num_pages

