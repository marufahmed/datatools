import pandas as pd

# Read CSV files into DataFrames
csv_big = pd.read_csv('errors_all.csv')
csv_small = pd.read_csv('errors20000.csv')

# Find unique rows in csv_big that are not in csv_small
unique_rows = csv_big.merge(csv_small, indicator=True, how='left').loc[lambda x: x['_merge'] == 'left_only'].drop('_merge', axis=1)

# Write unique rows to a new CSV file
unique_rows.to_csv('unique_rows.csv', index=False, encoding='utf-8-sig')
