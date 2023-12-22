import pandas as pd
import Levenshtein as lev

# Read the CSV file
file_path = 'result_ccw_word.csv'
data = pd.read_csv(file_path)

# Convert columns to strings
data['Text_GT'] = data['Text_GT'].astype(str)
data['Text_Pred'] = data['Text_Pred'].astype(str)

# Calculate Levenshtein distance
data['Levenshtein_Distance'] = data.apply(lambda row: lev.distance(str(row['Text_GT']), str(row['Text_Pred'])), axis=1)

# Adjust the score to a 0-100 range
max_distance = max(data['Levenshtein_Distance'])
data['Adjusted_Score'] = data['Levenshtein_Distance'].apply(lambda x: 100 - ((x / max_distance) * 100))

# Save the updated data to a new CSV file
data.to_csv('levenshtein_result_ccw_word.csv', index=False, encoding='utf-8-sig')

