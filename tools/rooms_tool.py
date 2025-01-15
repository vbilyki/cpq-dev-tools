import requests
import datetime

BASE_URL = "https://api.pandadoc.com/api/rooms/rooms/"

def create_room(template_id, name, api_key):
    """Create a PandaDoc Room using a specified template ID and name."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "template_uuid": template_id,
        "name": name
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code == 201:
        print("Room created successfully:")
        print(response.json())
        return response.json()
    else:
        print("Failed to create room:")
        print(f"Status Code: {response.status_code}")
        print(response.text)
        response.raise_for_status()
