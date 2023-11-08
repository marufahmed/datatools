import pandas as pd
import pyarrow.parquet as pq

while True:
    # Input Parquet file from the user
    parquet_file = input("Enter the Parquet file name (or 'exit' to quit): ")
    
    if parquet_file.lower() == 'exit':
        print("Exiting the program.")
        break

    try:
        # Read Parquet file
        table = pq.read_table(parquet_file)

        # Convert the Parquet table to a Pandas DataFrame
        df = table.to_pandas()

        # Determine the CSV file name based on the Parquet file name
        csv_file = parquet_file.replace('.parquet', '.csv')

        # Write the DataFrame to a CSV file
        df.to_csv(csv_file, index=False)  # Set index to False to exclude row numbers

        print(f"Data from '{parquet_file}' has been converted to '{csv_file}'")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

print("Program has finished.")

