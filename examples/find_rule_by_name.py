import os
from tools.workflow_tool import get_workflow, find_quote_id_by_name
from tools.rules_tool import get_all_rules_for_quote, get_rule_by_uuid

API_KEY = os.getenv("PANDADOC_API_KEY")
template_id = "ba619bc4-2a75-4c68-beb9-2f82b1ccab24"  # Replace with your template ID
quote_name = "Line items from opp 2"  # Replace with your quote name
rule_name = "List price < sales price "  # Replace with the rule name you are searching for

def find_rule_by_name():

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
        exit("No rules found for the specified quote.")

    # Search for the rule by name
    for rule in all_rules:
        if rule.get("name") == rule_name:
            rule_id = rule.get("uuid")
            if rule_id:
                # Fetch rule details
                rule_details = get_rule_by_uuid(rule_id, API_KEY)
                print("Rule found with details:")
                print(rule_details)
                return

    print(f"Rule with name '{rule_name}' not found.")

if __name__ == "__main__":
    find_rule_by_name()
