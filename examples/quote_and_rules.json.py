import os
import re

from tools.rules_parse_tool import find_reference_values_and_data_fields
from tools.rules_tool import get_all_rules_for_quote, get_rule_by_uuid
from tools.workflow_tool import get_workflow, find_quote_settings_by_name
from tools.quote_tool import get_quote, get_quote_token
from schemas.integration.quote_with_rules import IntegrationQuote

API_KEY = os.getenv("PANDADOC_API_KEY")
template_id = "fbc21d17-3147-4928-a328-d5ab77068637"
quote_name = "Create a quote"


def get_integration_quote():
    # Fetch workflow data
    workflow_data = get_workflow(template_id, API_KEY)
    if not workflow_data:
        exit("Failed to fetch workflow.")

    # Find the quote ID and quote version
    quote_id, version_id = find_quote_settings_by_name(workflow_data, quote_name)
    if not quote_id:
        exit(f"Quote with name '{quote_name}' not found.")
    if not version_id:
        exit(f"Quote with name '{quote_name}' and version '{version_id}' not found.")

    print(f"Found Quote ID: {quote_id} with version: {version_id}")

    # Fetch quote toke
    quote_token = get_quote_token(template_id, quote_id, API_KEY)
    # Fetch quote using quote token
    quote = get_quote(quote_id, version_id, quote_token, API_KEY)
    # Fetch rule details and save to the list
    rules = [get_rule_by_uuid(rule["uuid"], API_KEY) for rule in get_all_rules_for_quote(quote_id, API_KEY)]

    # Parse quote together with rules
    integration_quote = IntegrationQuote.from_dict(quote, rules)

    # Print some usefull information
    print(f"Quote data fields: {integration_quote.data_fields}")
    print(f"Quote columns: {[section.columns for section in integration_quote.sections]}")
    print(f"Section totals: {[section.totals for section in integration_quote.sections]}")
    print(f"Rules: [{integration_quote.rules}]")

    # Check if all rules refers to the existing data field
    return integration_quote


def extract_after_prefix(path: str, prefix: str) -> list[str]:
    """
    Extracts all substrings that follow a specific prefix in a given path.
    Args:
        path (str): The nested path string to search, e.g., "[quote_ctx.quote.data_fields_map.to_delete] *[item_ctx.price]".
        prefix (str): The prefix to search for, e.g., "quote_ctx.quote.data_fields_map.".
    Returns:
        list[str]: A list of all substrings that follow the prefix.
    """
    pattern = re.escape(prefix) + r"([a-zA-Z0-9_]+)"  # Match prefix followed by an alphanumeric word
    matches = re.findall(pattern, path)
    return matches


def get_not_existed_attribute_from_rules(
    quote, attribute_type='data_field', attribute_prefix="quote_ctx.quote.data_fields_map."
) -> dict("attr_name", "rule_name"):
    not_existed_attributes = {}
    if attribute_type == "data_filed":
        current_quote_attribute_names = {df.name for df in quote.data_fields}

    for rule in quote.rules:
        # Check 'when' and 'then' lookups for each rule
        for lookup in (
            find_reference_values_and_data_fields(rule.when),
            find_reference_values_and_data_fields(rule.then),
        ):
            for reference in lookup:
                if reference and attribute_prefix in reference:
                    # Extract the data field name
                    attr_name = extract_after_prefix(reference, attribute_prefix)[0]
                    # Check if the data field exists in the quote
                    if attr_name not in current_quote_attribute_names:
                        if attr_name not in not_existed_attributes:
                            not_existed_attributes[attr_name] = []
                        not_existed_attributes[attr_name].append({rule.name: rule.uuid})

    return not_existed_attributes


def check_rules_refers_to_exist_data_field(quote: IntegrationQuote):
    missing_data_fields = get_not_existed_attribute_from_rules(quote)
    # Print any missing data fields with associated rule names
    if missing_data_fields:
        red_color = "\033[31m"
        reset_color = "\033[0m"
        for data_field, rules in missing_data_fields.items():
            rule_list = ", ".join(rules)
            print(
                f"{red_color}Data field [{data_field}] which is not found in quote is used in rules: {rule_list}{reset_color}"
            )


def create_needed_data_fields_in_quote(quote, df_to_create):
    pass


if __name__ == "__main__":
    quote = get_integration_quote()
    check_rules_refers_to_exist_data_field(quote)
