import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_element(ax, element):
    element_type = element.get('type', '')
    points = element.get('points', [])

    if element_type == 'TextBlock' and points:
        x_values = [point['x'] for point in points]
        y_values = [point['y'] for point in points]

        rect = patches.Polygon(xy=list(zip(x_values, y_values)), closed=True, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        text = element.get('text', {}).get('0', '')
        ax.text(x_values[0], y_values[0], text, fontsize=8, color='b')

    elif element_type == 'paragraph' and points:
        # Handle paragraph type, if needed
        pass

    # Add more conditions for other element types if necessary

def visualize_json(json_data):
    fig, ax = plt.subplots()

    for segment_id, element in json_data.get('segments', {}).items():
        draw_element(ax, element)

    plt.xlim(0, json_data.get('width', 1))
    plt.ylim(0, json_data.get('height', 1))
    plt.gca().invert_yaxis()  # Invert y-axis to match the coordinate system

    plt.show()

def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

# Specify the path to your JSON file
json_file_path = 'layout.json'

# Load JSON data from the file
json_data = load_json_from_file(json_file_path)

# Visualize the JSON data
visualize_json(json_data)
