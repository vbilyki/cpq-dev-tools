import os
from tools.quote_tool import get_workflow, find_quote_id_by_name
from tools.rules_tool import get_all_rules_for_quote, delete_rule

API_KEY = os.getenv("PANDADOC_API_KEY")
template_id = "a3a5e9ba-b005-4396-a91e-d17d00025746"
quote_name = "Create a quote"

def delete_all_rules_example():

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
        return

    # Delete all rules
    for rule in all_rules:
        rule_id = rule.get("uuid")
        if rule_id:
            delete_rule(rule_id, API_KEY)
            print(f"Deleted rule with UUID: {rule_id}")

    print("All rules deleted successfully.")

if __name__ == "__main__":
    delete_all_rules_example()
