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
    _keys = [
        "children",
        "tag",
        "attributes",
        "frontmatter",
        "parent_attributes",
    ]
    
    def __init__(self, *,
                 children=None, tag=None, attributes=None,
                 frontmatter=None, parent_attributes=None):
        self.tag = tag if tag else {}
        self.attributes = attributes if attributes else {}
        self.frontmatter = frontmatter if frontmatter else {}
        self.parent_attributes = parent_attributes if parent_attributes else {}
        self.children = children if children else NodeList()

    @staticmethod
    def _comp(a, b):
        return (not a and not b) or a == b

    def __eq__(self, other):
        for key in self._keys:
            if not self._comp(getattr(self, key), getattr(other, key)):
                return False
        return True
