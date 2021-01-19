from dataclasses import dataclass
from typing import List


@dataclass
class ImportNode:
    tag: str
    attributes: dict
    children: List['ImportNode']