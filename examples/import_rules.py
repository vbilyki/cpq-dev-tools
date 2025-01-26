import os
from api.workflow_api import get_workflow
from tools.rules_tool import import_rules_from_csv
from tools.workflow_tool import find_quote_id_by_name

API_KEY = os.getenv("PANDADOC_API_KEY")
template_id = "a3a5e9ba-b005-4396-a91e-d17d00025746"
quote_name = "Create a quote 2"
input_file = "exported_rules.csv"


def import_rules_example():

    # Fetch workflow data
    workflow_data = get_workflow(template_id, API_KEY)
    if not workflow_data:
        exit("Failed to fetch workflow.")

    # Find the quote ID
    quote_id = find_quote_id_by_name(workflow_data, quote_name)
    if not quote_id:
        exit(f"Quote with name '{quote_name}' not found.")

    print(f"Found Quote ID: {quote_id}")

    # Import rules from CSV
    import_rules_from_csv(input_file, quote_id, API_KEY)

    print("Rules imported successfully from the CSV file.")


if __name__ == "__main__":
    import_rules_example()
