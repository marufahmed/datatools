# import csv
# from datetime import datetime

# with open('logo_detection.txt', 'r') as f:
#     lines = f.readlines()

# times = []
# for i in range(0, len(lines), 5):
#     if lines[i].strip() == '':
#         continue
#     start_time_str = lines[i][:23].strip()
#     end_time_str = lines[i+3][:23].strip()
#     start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     time_diff = end_time - start_time
#     times.append(time_diff.total_seconds())

# with open('logo_detection_times.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for i, time in enumerate(times):
#         writer.writerow([f'image {i+1}', f'time {time:.2f}'])

# import csv
# from datetime import datetime

# with open('recognition.txt', 'r') as f:
#     lines = f.readlines()

# times = []
# for i in range(0, len(lines), 4):
#     if lines[i].strip() == '':
#         continue
#     start_time_str = lines[i][:23].strip()
#     end_time_str = lines[i+3][:23].strip()
#     start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     time_diff = end_time - start_time
#     times.append(time_diff.total_seconds())

# with open('recognition_times.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for i, time in enumerate(times):
#         writer.writerow([f'image {i+1}', f'time {time:.2f}'])


# import csv
# from datetime import datetime

# with open('noise_removal.txt', 'r') as f:
#     lines = f.readlines()

# times = []
# i = 0
# while i < len(lines):
#     if lines[i].strip() == '':
#         i += 1
#         continue
#     start_time_str = lines[i][:23].strip()
#     end_time_str = lines[i+6][:23].strip()
#     start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     time_diff = end_time - start_time
#     times.append(time_diff.total_seconds())
#     i += 8

# with open('noise_removal_times.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for i, time in enumerate(times):
#         writer.writerow([f'image {i+1}', f'time {time:.2f}'])

# import csv
# from datetime import datetime

# with open('segmentation.txt', 'r') as f:
#     lines = f.readlines()

# times = []
# for i in range(0, len(lines), 5):
#     if lines[i].strip() == '':
#         continue
#     start_time_str = lines[i][:23].strip()
#     end_time_str = lines[i+3][:23].strip()
#     start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S.%f')
#     time_diff = end_time - start_time
#     times.append(time_diff.total_seconds())

# with open('segmentation_times.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for i, time in enumerate(times):
#         writer.writerow([f'image {i+1}', f'time {time:.2f}'])

import csv

# Read the data from the four CSV files
noise_removal_times = {}
with open('noise_removal_times.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        noise_removal_times[row[0]] = float(row[1].split()[-1])

logo_detection_times = {}
with open('logo_detection_times.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        logo_detection_times[row[0]] = float(row[1].split()[-1])

segmentation_times = {}
with open('segmentation_times.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        segmentation_times[row[0]] = float(row[1].split()[-1])

recognition_times = {}
with open('recognition_times.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        recognition_times[row[0]] = float(row[1].split()[-1])

# Combine the data into a single CSV file
with open('combined_times.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['image', 'noise_time', 'logo_time', 'segmentation_time', 'recognition_time', 'total_time'])
    for image in noise_removal_times:
        noise_time = noise_removal_times[image]
        logo_time = logo_detection_times.get(image, 0)
        segmentation_time = segmentation_times.get(image, 0)
        recognition_time = recognition_times.get(image, 0)
        total_time = noise_time + logo_time + segmentation_time + recognition_time
        writer.writerow([image, f'{noise_time:.2f}', f'{logo_time:.2f}', f'{segmentation_time:.2f}', f'{recognition_time:.2f}', f'{total_time:.2f}'])