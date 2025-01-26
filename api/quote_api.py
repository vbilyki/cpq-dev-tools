from uuid import uuid4

from api.api_client import make_request

BASE_URL = "https://api.pandadoc.com/api"


def get_quote_token_from_process(workflow_id, quote_id, api_key):
    url = f"{BASE_URL}/processes/constructor/templates/{workflow_id}/quotes/{quote_id}/quote_token"
    return make_request("GET", url, api_key)['quote_token']


def get_quote(quote_id, version_id, quote_token, api_key):
    url = f"{BASE_URL}/quotes/{quote_id}/{version_id}"
    headers = {"x-access-token": quote_token}
    return make_request("GET", url, api_key, headers=headers)


def update_quote(quote_data, quote_token, api_key):
    url = f"{BASE_URL}/quotes/{quote_data['uuid']}/{quote_data['version_id']}"
    headers = {"x-access-token": quote_token}
    payload = {"version_id": str(uuid4())}
    payload.update(quote_data)
    return make_request("PUT", url, api_key, json=payload, headers=headers)
