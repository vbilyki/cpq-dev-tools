import datetime
import os
from tools.workflow_tool import get_workflow, find_quote_id_by_name
from tools.rules_tool import create_rule, get_all_rules_for_quote, get_rule_by_uuid, delete_rule

API_KEY = os.getenv("PANDADOC_API_KEY")
template_id = "a3a5e9ba-b005-4396-a91e-d17d00025746"
quote_name = "Create a quote"

def main():

    # Fetch workflow and quote ID
    workflow_data = get_workflow(template_id, API_KEY)
    if not workflow_data:
        exit("Failed to fetch workflow.")

    quote_id = find_quote_id_by_name(workflow_data, quote_name)
    if not quote_id:
        exit(f"Quote with name '{quote_name}' not found.")

    print(f"Found Quote ID: {quote_id}")

    # Generate 50 rules
    for i in range(1, 51):
        rule_name = f"If quantity is {i} then price is {i}"
        when_clause = {
            "alias": {"id": "line-items-1", "name": "Line items 1", "return_type": "line-items"},
            "fn": {
                "left": {"value": {"value": "item_ctx.qty", "op": "$lookup"}, "op": "$int"},
                "right": {"value": str(i), "op": "$int"},
                "op": "$eq"
            },
            "data": {"value": "quote_ctx.quote.sections.items", "op": "$lookup"},
            "op": "$contains"
        }
        then_clause = {
            "fn": {
                "op": "$cmd",
                "name": "upsert_quote_line_item_field_value",
                "args": {
                    "line_item_id": {"value": "item_ctx.id", "op": "$lookup"},
                    "line_item_updated_fields": {"price": str(i)}
                }
            },
            "data": {"value": "alias.line-items-1", "op": "$lookup"},
            "op": "$map"
        }
        create_rule(quote_id, rule_name, when_clause, then_clause, API_KEY)

    # Fetch and print all rules
    all_rules = get_all_rules_for_quote(quote_id, API_KEY)
    for rule in all_rules:
        print(rule)

    # Fetch and print a specific rule
    if all_rules:
        specific_rule = get_rule_by_uuid(all_rules[0]["uuid"], API_KEY)
        print(specific_rule)

    # Delete a specific rule
    if all_rules:
        delete_rule(all_rules[0]["uuid"], API_KEY)

if __name__ == "__main__":
    main()
