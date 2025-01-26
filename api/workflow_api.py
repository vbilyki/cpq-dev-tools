from api.api_client import make_request
from tools.workflow_tool import find_quote_settings_by_name

BASE_URL = "https://api.pandadoc.com/api"


def get_workflow(template_id, api_key):
    url = f"{BASE_URL}/processes/constructor/templates/{template_id}"
    return make_request("GET", url, api_key)

def fetch_quote_settings_from_workflow(template_id, quote_name, api_key):
    """Fetch quote and associated rules from a workflow."""
    workflow_data = get_workflow(template_id, api_key)
    if not workflow_data:
        raise ValueError(f"Failed to fetch workflow for template_id: {template_id}")

    quote_id, version_id = find_quote_settings_by_name(workflow_data, quote_name)
    if not quote_id or not version_id:
        raise ValueError(f"Quote '{quote_name}' not found in workflow {template_id}.")

    return quote_id, version_id
