from typing import List
from dataclasses import dataclass


@dataclass
class ImportNode:
    tag: str
    attributes: dict
    children: List["ImportNode"]
