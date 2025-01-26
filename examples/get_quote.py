import os

from api.workflow_api import get_workflow
from api.quote_api import get_quote, get_quote_token_from_process
from schemas.quote_schema import Quote
from tools.workflow_tool import find_quote_settings_by_name

API_KEY = os.getenv("PANDADOC_API_KEY")
template_id = "fbc21d17-3147-4928-a328-d5ab77068637"
quote_name = "Create a quote"


def get_quote_data():
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
    quote_token = get_quote_token_from_process(template_id, quote_id, API_KEY)
    # Fetch quote using quote token
    quote = get_quote(quote_id, version_id, quote_token, API_KEY)
    quote_obj = Quote.from_dict(quote)

    print(f"Quote data fields: {quote_obj.data_fields}")
    print(f"Quote columns: {[section.columns for section in quote_obj.sections]}")
    print(f"Section totals: {[section.totals for section in quote_obj.sections]}")


if __name__ == "__main__":
    get_quote_data()
