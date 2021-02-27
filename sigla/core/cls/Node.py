from textwrap import dedent
from typing import Any
from sigla.core.cls.Attributes import Attributes
from sigla.core.cls.Data import Data
from sigla.utils import import_node_list

NodeList = import_node_list()


class Node(object):
    def __init__(self, tag, attributes=None):
        if attributes is None:
            attributes = {}
        self.data = Data(
            tag, attributes=attributes, children=[], parent_attributes={}
        )
        self.context = {}

    @property
    def attributes(self):
        return Attributes(
            self.data.frontmatter_attributes,
            self.data.attributes,
            self.data.parent_attributes,
        )

    def __getattr__(self, name: str) -> Any:
        if name in self.attributes:
            return self.attributes[name]
        raise AttributeError(f"{self.__class__.__name__}.{name} is invalid.")

    def __repr__(self) -> str:
        tag = self.data.tag
        attrs = self.attributes if len(self.attributes.keys()) > 0 else ""
        children = self.children if len(self.children) > 0 else ""
        return dedent(f"""<{tag} {attrs}>{children}</{self.data.tag}>""")

    def __eq__(self, other):
        return self.data == other.data

    def append(self, node: "Node"):
        self.data.children.append(node)
        return self

    def process(self):
        self.update_context()

    def __call__(self, *args, **kwargs):
        return self.process()

    def update_parent_context(self, ctx):
        self.data.parent_attributes.update(**ctx)

    def update_context(self):
        for child in self.data.children:
            ctx = self.context.copy()
            ctx.update(dict(self.attributes))
            child.update_parent_context(ctx)
            child.update_context()

    def flatten(self):
        return [self, *self.children.flatten()]

    @property
    def children(self):
        return NodeList(self.data.children)
