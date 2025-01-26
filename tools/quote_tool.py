from api.quote_api import get_quote_token_from_process, get_quote
from schemas.quote_schema import Quote


def get_quote_from_workflow(template_id, quote_id, version_id, api_key):
    quote_token = get_quote_token_from_process(template_id, quote_id, api_key)
    quote_data = get_quote(quote_id, version_id, quote_token, api_key)
    return Quote.from_dict(quote_data)
