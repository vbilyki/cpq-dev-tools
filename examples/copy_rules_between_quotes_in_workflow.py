import os
from time import perf_counter

from schemas.integration.quote_with_rules import IntegrationQuote
from tools.quote_tool import get_quote_token, get_quote
from tools.workflow_tool import get_workflow, find_quote_settings_by_name
from tools.rules_tool import create_rule, get_all_rules_for_quote, get_rule_by_uuid, change_sequence_index

API_KEY = os.getenv("PANDADOC_API_KEY")
DEFAULT_QUOTE_NAME = "Create a quote"


def measure_time(func):
    """Decorator to measure the execution time of functions."""

    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took: {perf_counter() - start:.2f} seconds")
        return result

    return wrapper


@measure_time
def fetch_quote_with_rules(template_id, quote_name, token=API_KEY):
    """Fetch quote and associated rules from a workflow."""
    workflow_data = get_workflow(template_id, token)
    if not workflow_data:
        raise ValueError(f"Failed to fetch workflow for template_id: {template_id}")

    quote_id, version_id = find_quote_settings_by_name(workflow_data, quote_name)
    if not quote_id or not version_id:
        raise ValueError(f"Quote '{quote_name}' not found in workflow {template_id}.")

    quote_token = get_quote_token(template_id, quote_id, token)
    quote_data = get_quote(quote_id, version_id, quote_token, token)
    rules = [get_rule_by_uuid(rule["uuid"], token) for rule in get_all_rules_for_quote(quote_id, token)]

    return IntegrationQuote.from_dict(quote_data, rules)


@measure_time
def get_missing_rules(original_rules, target_rules):
    """Identify rules from the original workflow missing in the target workflow."""
    target_rule_names = {rule.name for rule in target_rules}
    return [rule for rule in original_rules if rule.name not in target_rule_names]


@measure_time
def create_rules_in_target(rules_to_create, target_quote_id, token=API_KEY):
    """Create rules in the target workflow."""
    for rule in rules_to_create:
        created_rule = create_rule(target_quote_id, rule.name, rule.when, rule.then, token, is_active=rule.is_active)
        change_sequence_index(created_rule["rule"]["uuid"], token, rule.sequence_index)
        print(f"Created rule '{rule.name}' with sequence index {rule.sequence_index}")


def copy_rules_between_quotes_in_workflow_main(args):
    """Main logic for copying rules between workflows."""
    token = args.token
    print("Starting the process of copying rules...")

    original_quote = fetch_quote_with_rules(args.orig_workflow, args.orig_qname, token=token)
    target_quote = fetch_quote_with_rules(args.orig_workflow, args.targ_qname, token=token)

    rules_to_create = get_missing_rules(original_quote.rules, target_quote.rules)
    print(f"Number of rules to create: {len(rules_to_create)}")

    if not rules_to_create:
        print("No new rules to create. Both quotes are already synchronized.")
    else:
        create_rules_in_target(rules_to_create, target_quote.id, token=token)
        print("All rules have been successfully created.")


def add_copy_rules_arguments(parser):
    """Define command-line arguments for the `copy_rules` command."""
    parser.add_argument("-orig_workflow", help="The workflow ID of the original workflow.")
    parser.add_argument("-targ_workflow", help="The workflow ID of the target workflow.")
    parser.add_argument(
        "-orig_qname", default=DEFAULT_QUOTE_NAME, help="The name of the quote (default: 'Create a quote')."
    )
    parser.add_argument(
        "-targ_qname", default=DEFAULT_QUOTE_NAME, help="The name of the target quote (default: 'Create a quote')."
    )
