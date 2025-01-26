import os

from helpers.rules_helper import create_rules_in_target
from helpers.workflow_helper import fetch_quote_with_rules_from_workflow

from utils import measure_time

API_KEY = os.getenv("PANDADOC_API_KEY")
DEFAULT_QUOTE_NAME = "Create a quote"


@measure_time
def get_missing_rules(original_rules, target_rules):
    """Identify rules from the original workflow missing in the target workflow."""
    target_rule_names = {rule.name for rule in target_rules}
    return [rule for rule in original_rules if rule.name not in target_rule_names]


def copy_rules_between_quotes_in_workflow_main(args):
    """Main logic for copying rules between workflows."""
    token = args.token
    print("Starting the process of copying rules...")

    original_quote = fetch_quote_with_rules_from_workflow(args.orig_workflow, args.orig_qname, token)
    target_quote = fetch_quote_with_rules_from_workflow(args.orig_workflow, args.targ_qname, token)

    rules_to_create = get_missing_rules(original_quote.rules, target_quote.rules)
    print(f"Number of rules to create: {len(rules_to_create)}")

    if not rules_to_create:
        print("No new rules to create. Both quotes are already synchronized.")
    else:
        create_rules_in_target(rules_to_create, target_quote.id, token)
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
