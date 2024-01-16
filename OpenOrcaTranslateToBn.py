import pandas as pd
import requests
import time

# Load the CSV file
csv_path = 'OpenOrca.csv'  # Update with the path to your CSV file
df = pd.read_csv(csv_path)

# Set up LibreTranslate API endpoint
libretranslate_url = "http://localhost:5000/translate"  # Update with your LibreTranslate API endpoint

# Function to translate text using LibreTranslate API
def translate_text(text):
    try:
        response = requests.post(libretranslate_url, json={
            "q": text,
            "source": "en",
            "target": "bn"
        })
        response.raise_for_status()
        translated_text = response.json()["translatedText"]
        return translated_text
    except Exception as e:
        raise ValueError(f"Error translating text: {e}")

# Function to read the log file and get the last processed index
def read_log_file(log_file_path):
    try:
        log_df = pd.read_csv(log_file_path)
        last_processed_index = log_df['processed_rows'].max() + 1 if not log_df.empty else 0
        return last_processed_index
    except Exception as e:
        print(f"Error reading log file: {e}")
        return 0

# Translation loop
translated_pairs = 0
processed_rows_log = []

# Resume from the last processed index if log file exists
log_file_path = 'processed_rows_log.csv'
start_index = read_log_file(log_file_path)

for index, row in df.iterrows():
    if index < start_index:
        continue  # Skip rows that have already been processed

    question = row['question']
    response = row['response']

    try:
        # Translate question and response
        translated_question = translate_text(question)
        translated_response = translate_text(response)

        # Update the DataFrame with translated text
        df.at[index, 'question'] = translated_question
        df.at[index, 'response'] = translated_response

        translated_pairs += 1
        processed_rows_log.append(index)

        # Check if 30 minutes have passed and save progress
        if translated_pairs % 2 == 0:
            df.to_csv('translated_data.csv', index=False, encoding='utf-8-sig')
            log_df = pd.DataFrame({"processed_rows": processed_rows_log})
            log_df.to_csv(log_file_path, index=False, encoding='utf-8-sig')

    except Exception as e:
        print(f"Error translating pair at index {index}: {e}")

# Save the final DataFrame with only the last two rows
df_tail = df.tail(2)
df_tail.to_csv('translated_data_final.csv', index=False, encoding='utf-8-sig')

print("Translation completed. Total translated pairs:", translated_pairs)
