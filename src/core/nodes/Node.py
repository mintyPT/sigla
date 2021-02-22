from collections import ChainMap
from copy import deepcopy
from dataclasses import dataclass, field
from textwrap import dedent
from typing import Any


@dataclass
class BaseNode:
    """This data class is meant to hold the data for each node"""

    tag: str
    attributes: dict = field(default_factory=dict)
    frontmatter_attributes: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    parent_attributes: dict = field(default_factory=dict)


class Attributes(ChainMap):
    def without(self, name):
        data = deepcopy(dict(self))
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


class Node:
    def __init__(self, tag, attributes=None):
        if attributes is None:
            attributes = {}
        self.data = BaseNode(
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
        # print(f'node does not have attr {name}')
        raise AttributeError()

    def __repr__(self) -> str:
        tag = self.data.tag
        attrs = self.attributes if len(self.attributes.keys()) > 0 else ""
        children = self.children if len(self.children) > 0 else ""
        return dedent(
            f"""<{tag}  {attrs}>{children}</{self.data.tag}>
        """
        )

    def __eq__(self, other):
        return (
            self.data.tag == other.data.tag
            and self.data.attributes == other.data.attributes
            and self.data.children == other.data.children
        )  # and self.context == other.context

    def append(self, node: "Node"):
        self.data.children.append(node)
        return self

    def process(self):
        self.update_context()

    def __call__(self, *args, **kwargs):
        return self.process()

    def update_parent_context(self, ctx):
        self.data.parent_attributes.update(**ctx)
        pass

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


class NodeList(list):
    def __call__(self, sep="\n"):
        children = [c() for c in self]
        if sep:
            return sep.join(children)
        return children

    def flatten(self):
        ret = []
        for child in self:
            ret.append(*child.flatten())
        return NodeList(ret)

    def nonone(self):
        return NodeList(filter(lambda e: e is not None, self))

    def get(self, name):
        return NodeList(map(lambda e: getattr(e, name), self))

    def join(self, sep):
        return sep.join(self)
