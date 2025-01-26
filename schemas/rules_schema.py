from dataclasses import dataclass


@dataclass
class Rule:
    uuid: str
    name: str
    is_active: str
    when: dict
    then: dict
    sequence_index: int
