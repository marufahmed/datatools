import re
import csv

def filter_and_parse_log(input_file, csv_file):
    parsed_data = []

    with open(input_file, 'r') as f_in:
        for line in f_in:
            # Check if the line contains the specified strings
            if "Successfully Completed Recogntion." not in line and \
               "Produced to docx_text_reconstruct Queue." not in line:
                match_init = re.match(r".*? 'projectId': '(\d+)', 'fileName': '([^']+)'.*", line)
                match_info = re.match(r".* 'pipeline_time': ([\d.]+).*", line)

                if match_init:
                    project_id, file_name = match_init.group(1), match_init.group(2)
                    parsed_data.append({'projectId': project_id, 'fileName': file_name})
                elif match_info:
                    if parsed_data:
                        parsed_data[-1]['pipeline_time'] = match_info.group(1)

    # Write parsed data to CSV file
    with open(csv_file, 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=['projectId', 'fileName', 'pipeline_time'])
        writer.writeheader()
        writer.writerows(parsed_data)

# Specify the paths
input_file = 'recognition_q_small.log'
csv_file = 'output.csv'

# Call the function
filter_and_parse_log(input_file, csv_file)
