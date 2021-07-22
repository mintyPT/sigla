from collections import ChainMap
from typing import Any

from sigla.data.errors import DataKeyError


class Data(object):
    def __init__(self, tag, children=None, parent=None, **kwargs):
        if children is None:
            children = []
        self.tag = tag
        self.own_attributes = kwargs
        self.parent: Data = parent
        self.children = children
        for child in self.children:
            child.parent = self

    @property
    def attributes(self):
        return ChainMap(
            self.own_attributes,
            self.parent.attributes if self.parent else {},  # parent_attributes
        )

    def get(self, key, default=None):
        if key in self.attributes:
            return self.attributes[key]
        return default

    def __iter__(self):
        for child in self.children:
            yield child

    def __getattr__(self, name: str) -> Any:
        if name in self.attributes.keys():
            return self.attributes[name]
        if name == "children":
            return self.children
        raise DataKeyError(f"No data found for {name}")

    def same_own_attributes(self, other):

        if self.own_attributes.keys() != other.own_attributes.keys():
            return False

        for own_key, own_value in self.own_attributes.items():
            if own_value != other.own_attributes[own_key]:
                return False

        return True

    def __eq__(self, other):

        if (
            type(self) != type(other)
            or self.tag != other.tag
            or not self.same_own_attributes(other)
        ):
            return False

        if not (
            (not self.children and not other.children)
            or (self.children == other.children)
        ):
            return False

        return True

    def find_by_id(self, raw_id: str):

        if self.own_attributes.get("id") == raw_id:
            return self

        for child in self:
            found = child.find_by_id(raw_id)
            if found:
                return found

    def render(self, *, indent=0):
        spacer = " " * indent

        children = [child.render(indent=indent + 4) for child in self]
        flat = len(children) == 0

        if len(self.attributes.keys()) == 0:
            open_tag = f"<{self.tag}>"
            open_close_tag = f"<{self.tag}/>"
        else:
            attributes = " ".join(
                f'{k}="{v}"' for k, v in self.attributes.items()
            )
            open_tag = f"<{self.tag} {attributes}>"
            open_close_tag = f"<{self.tag} {attributes}/>"

        if flat:
            return f"{spacer}{open_close_tag}"

        ret = [f"{spacer}{open_tag}", *children, f"{spacer}</{self.tag}>"]

        return "\n".join(ret)
