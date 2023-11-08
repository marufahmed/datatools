# Parquet to CSV Converter

This is a simple Python program that converts Parquet files to CSV files. It utilizes the `pandas` and `pyarrow` libraries to read and write data.

## Prerequisites

Before using this program, ensure that you have Python installed on your system. You can install the required libraries using the following commands:

```bash
pip install pandas pyarrow
```

## Usage

1. Save the program in a Python file (e.g., `parquet_to_csv_converter.py`).

2. Run the program in your terminal or command prompt:

```bash
python parquet_to_csv_converter.py
```

3. Follow the instructions to convert Parquet files to CSV:

   - Enter the name of the Parquet file you want to convert.
   - Type 'exit' and press Enter to quit the program.

The program will read the Parquet file, convert it to a CSV file, and display the success message. If any errors occur during the conversion, the program will notify you.

## Notes

- Make sure the Parquet file is in the same directory as the program or provide the full path to the file.
- The CSV file will have the same name as the Parquet file, with the '.csv' extension.

## Example

Here's an example of how to use the program:

```bash
Enter the Parquet file name (or 'exit' to quit): data.parquet
Data from 'data.parquet' has been converted to 'data.csv'
Enter the Parquet file name (or 'exit' to quit): exit
Exiting the program.
Program has finished.
```

Enjoy converting your Parquet files to CSV effortlessly!


# PDF to JPG Converter

This is a Python script that converts PDF files into JPG images. It utilizes the `os`, `subprocess`, and `glob` libraries.

## Prerequisites

Before using this script, ensure that you have the `convert` and `pdfinfo` commands available on your system. These commands are typically provided by the ImageMagick and Poppler packages. You can install them using package managers like `apt`, `brew`, or `chocolatey`. For example, on Ubuntu, you can install them as follows:

```bash
sudo apt-get install imagemagick
sudo apt-get install poppler-utils
```

## Usage

1. Save the script in a Python file (e.g., `pdf_to_jpg_converter.py`).

2. Specify the folder containing your PDF files by modifying the `pdf_folder` variable:

```python
pdf_folder = "/path/to/your/pdf/folder"
```

3. Run the script in your terminal or command prompt:

```bash
python pdf_to_jpg_converter.py
```

The script will convert the PDF files in the specified folder to JPG images and assign sequential index numbers to the output images.

## Notes

- Make sure to customize the `pdf_folder` variable with the path to your PDF files.
- The script uses the `convert` command to convert PDF files to JPG. If you encounter issues with the command, make sure ImageMagick is correctly installed.
- The `pdfinfo` command is used to determine the number of pages in each PDF.

## Example

Here's an example of how to use the script:

```bash
Converted 'file1.pdf' to '0.jpg'
Converted 'file2.pdf' to '3.jpg'
Converted 'file3.pdf' to '8.jpg'
```

Your PDF files will be converted into JPG images with sequential index numbers. Enjoy converting your PDFs to images!

