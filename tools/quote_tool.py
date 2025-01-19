from tools.api_client import make_request

BASE_URL = "https://api.pandadoc.com/api"


def get_quote_token(workflow_id, quote_id, api_key):
    url = f"{BASE_URL}/processes/constructor/templates/{workflow_id}/quotes/{quote_id}/quote_token"
    return make_request("GET", url, api_key)['quote_token']


def get_quote(quote_id, version_id, quote_token, api_key):
    url = f"{BASE_URL}/quotes/{quote_id}/{version_id}"
    headers = {"x-access-token": quote_token}
    return make_request("GET", url, api_key, headers=headers)


# quote token
# https://api.pandadoc.com/api/processes/constructor/templates/{proces_id}/quotes/{quote_id}/quote_token
# Request Method:
# GET
# response: {"quote_token": "sdasdas...."}


# get quote
# https://api.pandadoc.com/api/quotes/{quote_id}/{version_id}
# Request Method:
# GET
# x-access-token: {token from previous request}
