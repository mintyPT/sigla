from dataclasses import dataclass, field
from collections import ChainMap
from copy import deepcopy

from sigla.nodes.node_list import NodeList


class Attributes(ChainMap):
    def without(self, *args):
        data = deepcopy(dict(self))
        for name in args:
            del data[name]
        return Attributes(data)

    def as_kwargs(self, sep=","):
        kwargs = []
        for k, v in self.items():
            if type(v) == int:
                kwargs.append(f"{k}={v}")
            else:
                kwargs.append(f'{k}="{v}"')
        if sep:
            return ", ".join(kwargs)
        return kwargs


@dataclass
class Data:
    """This data class is meant to hold the data for each node"""

    tag: str

    attributes: dict = field(default_factory=dict)
    frontmatter_attributes: dict = field(default_factory=dict)
    parent_attributes: dict = field(default_factory=dict)

    children: list = field(default_factory=NodeList)
