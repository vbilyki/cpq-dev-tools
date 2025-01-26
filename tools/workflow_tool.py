def find_quote_id_by_name(workflow_data, quote_name):
    for step in workflow_data.get("steps", []):
        if step.get("type") == "quote" and step.get("name") == quote_name:
            return step.get("settings", {}).get("quote_id")


def find_quote_settings_by_name(workflow_data, quote_name):
    for step in workflow_data.get("steps", []):
        if step.get("type") == "quote" and step.get("name") == quote_name:
            return step.get("settings", {}).get("quote_id"), step.get("settings", {}).get("version_id")
