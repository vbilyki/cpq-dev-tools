from dataclasses import dataclass


@dataclass
class DataField:
    name: str
    type: str

    @classmethod
    def from_dict(cls, data_field: dict) -> "DataField":
        return DataField(name=data_field["name"], type=data_field["type"])

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
        }


@dataclass
class QuoteColumn:
    # id: str
    name: str
    type: str

    @classmethod
    def from_dict(cls, column: dict) -> "QuoteColumn":
        # looks like rules are using types to trace quote default column and
        # labels to trace through the custom columns
        if column["type"] == "text":
            name = column["label"]
        else:
            name = column["name"]
        return QuoteColumn(
            name=name,
            type=column["type"],
            #    id=column["id"]
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
        }


@dataclass
class SectionTotal:
    name: str
    type: str

    @classmethod
    def from_dict(cls, totals) -> "SectionTotal":
        return SectionTotal(name=totals["name"], type=totals["type"])

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
        }


@dataclass
class Section:
    columns: list[QuoteColumn]
    totals: list

    @classmethod
    def from_dict(cls, section: dict) -> "Section":
        columns = [QuoteColumn.from_dict(column) for column in section["line_item_fields"]]
        section_totals = [SectionTotal.from_dict(total) for total in section["fields"]]
        return Section(columns=columns, totals=section_totals)

    def to_dict(self) -> dict:
        return {
            "line_item_fields": [column.to_dict() for column in self.columns],
            "fields": [total.to_dict() for total in self.totals],
        }


@dataclass
class Quote:
    id: str
    version_id: str
    data_fields: list[DataField]
    sections: list[Section]

    @staticmethod
    def from_dict(quote: dict) -> "Quote":
        data_fields = [DataField.from_dict(field) for field in quote["data_fields"]]
        sections = [Section.from_dict(section) for section in quote["data_schema"]["sections"]]
        return Quote(
            id=quote["uuid"],
            version_id=quote["version_id"],
            data_fields=data_fields,
            sections=sections,
        )

    def to_dict(self) -> dict:
        return {
            "uuid": self.id,
            "version_id": self.version_id,
            "data_fields": [field.to_dict() for field in self.data_fields],
            "data_schema": {
                "sections": [section.to_dict() for section in self.sections],
            },
        }

    def get_unique_columns(self) -> list[QuoteColumn]:
        seen_names = set()
        unique_columns = []

        for section in self.sections:
            for column in section.columns:
                if column.name not in seen_names:
                    seen_names.add(column.name)
                    unique_columns.append(column)

        return unique_columns
