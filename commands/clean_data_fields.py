import os
from helpers.workflow_helper import fetch_quote_from_workflow
from api.quote_api import update_quote, get_quote_token_from_process


API_KEY = os.getenv("PANDADOC_API_KEY")
DEFAULT_QUOTE_NAME = "Create a quote"



def proceed_cleaning_data_fields(args):
    token = args.token
    original_quote = fetch_quote_from_workflow(args.orig_workflow,
                                               args.orig_qname, token)
    quote_token = get_quote_token_from_process(args.orig_workflow,
                                               original_quote['uuid'], token)

    data_fields = original_quote["data_fields"]
    found = False
    for df in data_fields:
        if df["value"]:
            found = True
            df["value"] = ""

    if found:
        updated_quote = original_quote.copy()
        updated_quote["data_fields"] = (data_fields)
        print(f"Updating quote {original_quote['uuid']}")

        try:
            update_quote(updated_quote, quote_token, token)
        except Exception as err:
            print(f"Error occured while updating quote: {err}")

        print(
            f"Quote [{original_quote['uuid']}] has been successfully updated. All data fields are empty right now. ")
    else:
        print("All data fields are empty. Nothing to update")

def clean_data_fields_main(args):
    """Main logic for copying rules between workflows."""
    quote_closed = input("Confirm that quote you are going to clean is closed. There is no any open instances of it. (y/n): ")

    if quote_closed.lower() in ["yes", "y", "ye"]:
        print("Starting the process of cleaning data fields...")
        proceed_cleaning_data_fields(args)

    else:
        print("Please, please close the quote and start command one more time")


def add_clean_data_fields_arguments(parser):
    """Define command-line arguments for the `copy_rules` command."""
    parser.add_argument("-orig_workflow", help="The workflow ID of the original workflow.")
    parser.add_argument(
        "-orig_qname", default=DEFAULT_QUOTE_NAME, help="The name of the quote (default: 'Create a quote')."
    )
