from typing import List


class BaseNode:
    tag: str
    attributes: dict
    children: List["BaseNode"]
    context: dict

    def __init__(self, tag, attributes=None):
        if attributes is None:
            attributes = {}
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.context = {}

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.attributes == other.attributes
            and self.children == other.children
        )  # and self.context == other.context

    def append(self, node: "BaseNode"):
        self.children.append(node)

    def process(self):
        self.update_context()

    def update_context(self):
        for child in self.children:
            ctx = self.context.copy()
            ctx.update(self.attributes.copy())
            child.context = ctx
            child.update_context()