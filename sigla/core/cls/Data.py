from dataclasses import dataclass, field


@dataclass
class Data:
    """This data class is meant to hold the data for each node"""

    tag: str
    attributes: dict = field(default_factory=dict)
    frontmatter_attributes: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    parent_attributes: dict = field(default_factory=dict)
