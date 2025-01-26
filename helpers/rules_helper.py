from api.rules_api import create_rule, change_sequence_index


def create_rules_in_target(rules_to_create, target_quote_id, api_key):
    """Create rules in the target workflow."""
    for rule in rules_to_create:
        created_rule = create_rule(target_quote_id, rule.name, rule.when, rule.then, api_key, is_active=rule.is_active)
        change_sequence_index(created_rule["rule"]["uuid"], api_key, rule.sequence_index)
        print(f"Created rule '{rule.name}' with sequence index {rule.sequence_index}")
