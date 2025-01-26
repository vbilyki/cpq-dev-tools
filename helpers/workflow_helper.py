from api.rules_api import get_rule_by_uuid, get_all_rules_for_quote
from api.workflow_api import fetch_quote_settings_from_workflow
from schemas.integration_quote_schema import IntegrationQuote
from tools.quote_tool import get_quote_from_workflow


def fetch_quote_with_rules_from_workflow(template_id, quote_name, qpi_key) -> IntegrationQuote:
    """Fetch quote and associated rules from a workflow."""
    print(f"Fetching quote {quote_name}")
    quote_id, version_id = fetch_quote_settings_from_workflow(template_id, quote_name, api_key=qpi_key)
    quote = get_quote_from_workflow(template_id, quote_id, version_id, qpi_key)
    rules = [get_rule_by_uuid(rule["uuid"], qpi_key) for rule in get_all_rules_for_quote(quote_id, qpi_key)]
    return IntegrationQuote.from_dict(quote, rules)


def fetch_quote_from_workflow(template_id, quote_name, api_key) -> dict:
    """Fetch quote"""
    quote_id, version_id = fetch_quote_settings_from_workflow(template_id, quote_name, api_key=api_key)
    return get_quote_from_workflow(template_id, quote_id, version_id, api_key)
