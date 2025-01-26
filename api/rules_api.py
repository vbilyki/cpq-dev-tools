import csv
import uuid
import json
from api.api_client import make_request

BASE_URL = "https://api.pandadoc.com/api"


def create_rule(quote_id, rule_name, when_clause, then_clause, api_key, is_active=True):
    url = f"{BASE_URL}/rules/"
    payload = {
        "uuid": str(uuid.uuid4()),
        "name": rule_name,
        "is_active": is_active,
        "linked_entity": {"entity_type": "quote", "id": quote_id},
        "when": when_clause,
        "then": then_clause,
    }
    return make_request("POST", url, api_key, json=payload)


def get_all_rules_for_quote(quote_id, api_key):
    url = f"{BASE_URL}/rules/quote/{quote_id}"
    return make_request("GET", url, api_key).get("rules", [])


def get_rule_by_uuid(rule_id, api_key):
    url = f"{BASE_URL}/rules/{rule_id}"
    return make_request("GET", url, api_key).get("rule", {})


def delete_rule(rule_id, api_key):
    url = f"{BASE_URL}/rules/{rule_id}"
    make_request("DELETE", url, api_key)


def change_sequence_index(rule_id, api_key, sequence_index):
    url = f"{BASE_URL}/rules/{rule_id}/sequence_index"
    payload = {"sequence_index": sequence_index}
    make_request("PATCH", url, api_key, json=payload)
