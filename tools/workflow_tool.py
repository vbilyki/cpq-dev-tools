from tools.api_client import make_request

BASE_URL = "https://api.pandadoc.com/api"

def get_workflow(template_id, api_key):
    url = f"{BASE_URL}/processes/constructor/templates/{template_id}"
    return make_request("GET", url, api_key)

def find_quote_id_by_name(workflow_data, quote_name):
    for step in workflow_data.get("steps", []):
        if step.get("type") == "quote" and step.get("name") == quote_name:
            return step.get("settings", {}).get("quote_id")
    return None
