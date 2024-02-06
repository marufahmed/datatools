import requests

def get_model_config(model_name, model_version=None):
    base_url = "http://localhost:8000/v2/models"
    url = f"{base_url}/{model_name}"
    if model_version:
        url += f"/versions/{model_version}"
    url += "/config"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch config for model '{model_name}' (version: {model_version}): {response.status_code} - {response.text}")
        return None

# Example usage
model_name = "ocr_layout"
model_version = "1"  # Optional, set to None if the model doesn't have versions
config = get_model_config(model_name, model_version)
if config:
    print(config)
