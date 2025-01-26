from dataclasses import dataclass
from schemas.quote_schema import Quote, Section, DataField
from schemas.rules_schema import Rule


@dataclass
class IntegrationQuote:
    id: str
    version_id: str
    data_fields: list[DataField]
    sections: list[Section]
    rules: list[Rule]

    @staticmethod
    def from_dict(quote: Quote, rules: list) -> "IntegrationQuote":
        # Create and return the IntegrationQuote object
        return IntegrationQuote(
            id=quote.id,
            version_id=quote.version_id,
            data_fields=quote.data_fields,
            sections=quote.sections,
            rules=[
                Rule(
                    uuid=rule["uuid"],
                    name=rule["name"],
                    is_active=rule["is_active"],
                    when=rule["when"],
                    then=rule["then"],
                    sequence_index=rule["sequence_index"],
                )
                for rule in rules
            ],
        )
