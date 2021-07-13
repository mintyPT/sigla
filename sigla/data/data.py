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


class Data(object):
    _meta = [
        {"name": "children"},
        {"name": "tag"},
        {"name": "attributes"},
        {"name": "parent_attributes"},
        {"name": "frontmatter"},
    ]

    def __init__(
        self,
        *,
        children=None,
        tag=None,
        attributes=None,
        parent_attributes=None,
        frontmatter=None,
    ):
        self.tag = tag if tag else {}
        self.children = children if children else NodeList()

        self.attributes = attributes if attributes else {}
        self.parent_attributes = parent_attributes if parent_attributes else {}
        self.frontmatter = frontmatter if frontmatter else {}

    @staticmethod
    def _comp(a, b):
        return (not a and not b) or a == b

    def __eq__(self, other):
        for key in self._meta:
            self_value = getattr(self, key["name"])
            other_value = getattr(other, key["name"])

            if not self._comp(self_value, other_value):
                return False

        return True

    def get_attributes(self):
        return Attributes(
            self.frontmatter, self.attributes, self.parent_attributes
        )
