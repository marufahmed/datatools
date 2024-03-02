import json

def print_json_structure(data, indent=2):
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{' ' * indent}'{key}':")
            print_json_structure(value, indent + 2)
    elif isinstance(data, list):
        for item in data:
            print_json_structure(item, indent)
    else:
        print(f"{' ' * indent}{data}")

def main():
    # Replace 'your_large_json_file.json' with the path to your actual JSON file
    json_file_path = 'layout.json'

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        print("JSON Structure:")
        print_json_structure(json_data)

    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    main()

