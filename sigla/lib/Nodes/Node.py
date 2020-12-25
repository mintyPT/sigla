from typing import Dict, Union, List
import pydash as _

from sigla.lib.helpers.Context import Context


class Node(object):
    attributes: Dict[str, Union[str, int]] = {}
    meta: Dict[str, Union[str, int]] = {}
    children: List["Node"] = []
    kind = "node"

    def is_(self, what):
        return self.kind == what

    def flatten(self):
        return _.flatten(
            [self, *list(map(lambda e: e.flatten(), self.children))]
        )

    def __init__(
        self, children: List["Node"] = None, attributes=None, meta=None
    ):
        if children is None:
            children = []
        if attributes is None:
            attributes = {}
        if meta is None:
            meta = {}

        self.attributes = attributes
        self.meta = meta
        self.children = children

    @classmethod
    def meta_from_node(cls, node):
        meta = {
            "tag": node.tag.split("-")[-1],
            "otag": node.tag,  # otag => original tag
        }
        return meta

    @classmethod
    def attributes_from_node(cls, node):
        attributes = {}
        for k, v in node.attrib.items():
            if k.endswith("-int"):
                attributes[k.replace("-int", "")] = int(v)
            else:
                attributes[k] = v
        return attributes

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError as e:
            if name in self.attributes.keys():
                return self.attributes[name]
            elif name in self.meta.keys():
                return self.meta[name]
            else:
                raise e

    def __iter__(self):
        return iter(self.children)

    def get_template_name(self):
        return self.otag

    def process(self, ctx: Context = None):
        raise NotImplementedError("Implement this method")
