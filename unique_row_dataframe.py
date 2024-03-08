
import csv
import re

def extract_info(line):
    pattern = r"'(\w+)':\s*(?:'([^']*)'|([^,}]+))"
    info = {}
    matches = re.findall(pattern, line)
    for match in matches:
        key = match[0]
        value = match[1] if match[1] else match[2]
        info[key] = value.strip()
    return info

def extract_timings(line):
    pattern = r"Timings: (.+)}"
    match = re.search(pattern, line)
    timings = {}
    if match:
        timings_str = match.group(1)
        timings_list = timings_str.split(", ")
        for item in timings_list:
            key, value = item.split(': ')
            timings[key.strip()] = float(value)
    return timings

def log_to_csv(log_file, csv_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()

    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'id', 'projectId', 'fileName', 'targetedStatus', 
                      'requestLevel', 'documentType', 'isNewspaper', 'ocrModelType', 
                      'keepEnglish', 'pdfImageExtractToResize', 'read_img_time', 
                      'english_remover_time', 'recognition_time', 'pipeline_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        init_info = {}
        timings_info = {}
        produced_info = {}
        for line in lines:
            if 'INIT' in line:
                init_info = extract_info(line)
            elif 'Produced to docx_text_reconstruct Queue' in line:
                produced_info = extract_info(line)
                writer.writerow({**init_info, **timings_info, **produced_info})
            elif 'Timings:' in line:
                timings_info = extract_timings(line)

# Example usage
log_file = 'recognition_q.log'
csv_file = 'recognition_q.csv'
log_to_csv(log_file, csv_file)
