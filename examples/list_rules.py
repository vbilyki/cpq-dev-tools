import json
import os
from tools.workflow_tool import get_workflow, find_quote_id_by_name
from tools.rules_tool import get_all_rules_for_quote

API_KEY = os.getenv("PANDADOC_API_KEY")
template_id = "a3a5e9ba-b005-4396-a91e-d17d00025746"
quote_name = "Create a quote"

def list_rules():
    # Fetch workflow data
    workflow_data = get_workflow(template_id, API_KEY)
    if not workflow_data:
        exit("Failed to fetch workflow.")

    # Find the quote ID
    quote_id = find_quote_id_by_name(workflow_data, quote_name)
    if not quote_id:
        exit(f"Quote with name '{quote_name}' not found.")

    print(f"Found Quote ID: {quote_id}")

    # Fetch all rules for the quote
    all_rules = get_all_rules_for_quote(quote_id, API_KEY)

    if not all_rules:
        print("No rules found for the specified quote.")
    else:
        print("Listing all rules for the quote:")
        for rule in all_rules:
            print(json.dumps(rule, indent=4))

if __name__ == "__main__":
    list_rules()
