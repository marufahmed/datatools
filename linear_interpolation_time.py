from datetime import datetime, timedelta

# Define start and end time
start_time = datetime.strptime('10:13:03', '%H:%M:%S')
end_time = datetime.strptime('10:14:04', '%H:%M:%S')

# Calculate the time difference
time_diff = end_time - start_time

# Calculate the interval between timestamps
interval = time_diff.total_seconds() / 43

# Generate timestamps
timestamps = []
current_time = start_time
for _ in range(44):
    timestamps.append(current_time.strftime('%H:%M:%S'))
    current_time += timedelta(seconds=interval)

# Print the timestamps
for timestamp in timestamps:
    print(timestamp)

