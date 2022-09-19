from dataclasses import dataclass
from typing import Dict


@dataclass
class Request:
    function: str
    arguments: Dict[str, str]

    @staticmethod
    def from_dict(dictionary) -> "Request":
        return Request(function=dictionary["function"], arguments=dictionary["arguments"])
