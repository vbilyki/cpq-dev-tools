import csv
import uuid
import json
from tools.api_client import make_request

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


def export_rules_to_csv(rules, csv_file_path, api_key):
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["UUID", "Name", "Is Active", "Sequence Index", "Created At", "Updated At", "When", "Then"])

        # Write rule data
        for rule in rules:
            rule_details = get_rule_by_uuid(rule.get("uuid"), api_key)
            writer.writerow(
                [
                    rule_details.get("uuid"),
                    rule_details.get("name"),
                    rule_details.get("is_active"),
                    rule_details.get("sequence_index"),
                    rule_details.get("created_at"),
                    rule_details.get("updated_at"),
                    json.dumps(rule_details.get("when"), indent=4) if rule_details.get("when") else "null",
                    json.dumps(rule_details.get("then"), indent=4) if rule_details.get("then") else "null",
                ]
            )

    print(f"Rules exported successfully to {csv_file_path}")


def import_rules_from_csv(csv_file_path, quote_id, api_key):
    with open(csv_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rule_name = row["Name"]
            is_active = row["Is Active"] == "True"

            when_clause = json.loads(row["When"])
            then_clause = json.loads(row["Then"])

            create_rule(quote_id, rule_name, when_clause, then_clause, api_key)

    print(f"Rules imported successfully from {csv_file_path}")
