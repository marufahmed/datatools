import gzip
import shutil

def gunzip_file(gzipped_file, output_file):
    with gzip.open(gzipped_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

gzipped_file = '/Users/marufahmed/Downloads/2023.csv.gz'
output_file = '/Users/marufahmed/Downloads/2023.csv'

gunzip_file(gzipped_file, output_file)

