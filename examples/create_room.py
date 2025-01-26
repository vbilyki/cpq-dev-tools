from api.rooms_api import create_room
import os
import datetime

API_KEY = os.getenv("PANDADOC_API_KEY")
template_id = "438c11dd-9a0a-451c-aeaf-9ae19395d586"
current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
room_name = f"Template created via API {current_timestamp}"


def create_room_example():
    if not API_KEY:
        print("PANDADOC_API_KEY environment variable is not set.")
        return

    create_room(template_id, room_name, API_KEY)


if __name__ == "__main__":
    create_room_example()
