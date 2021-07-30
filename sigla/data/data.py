from collections import ChainMap
from typing import Any
from typing import ChainMap as TChainMap
from typing import Generator, List, Optional, Union
from helpers.helpers import join
from sigla.data.data_finder import DataFinder
from sigla.engines.helpers.helpers import as_kwargs


class Data:
    parent: Optional["Data"]

    def __init__(
            self,
            tag: str,
            children: Optional[List["Data"]] = None,
            parent: Optional["Data"] = None,
            **kwargs,
    ) -> None:
        if children is None:
            children = []
        self.tag = tag
        self.own_attributes = kwargs
        self.parent: Data = parent
        self.children = children
        for child in self.children:
            child.parent = self

    def duplicate(self, **kwargs: Any) -> "Data":
        data = {
            "parent": self.parent,
            "children": [c.duplicate() for c in self.children],
            **self.own_attributes,
            **kwargs,
        }

        return Data(self.tag, **data)

    @property
    def attributes(self) -> TChainMap:
        return ChainMap(
            self.own_attributes,
            self.parent.attributes if self.parent else {},  # parent_attributes
        )

    def get(self, key: str, default: Any = None) -> Any:
        if key in self.attributes:
            return self.attributes[key]
        return default

    def __iter__(self) -> Generator:
        for child in self.children:
            yield child

    def __getattr__(self, name: str) -> Any:
        if name in self.attributes.keys():
            return self.attributes[name]
        raise AttributeError(name)

    def same_own_attributes(self, other: Any) -> bool:

        if self.own_attributes.keys() != other.own_attributes.keys():
            return False

        for own_key, own_value in self.own_attributes.items():
            # TODO instead of type(own_value) != Data check if one of them is self?
            # When we replace by id, we will receive a reference to ourselves
            # type(own_value) != Data
            if (
                    own_value != other.own_attributes[own_key]
                    and type(own_value) != Data
            ):
                return False

        return True

    def __eq__(self, other: Any) -> bool:

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

    def find_by_id(self, raw_id: str) -> Union[None, Any]:
        finder = DataFinder(self)
        return finder.find_by_id(raw_id)

    def render(self, *, indent: int = 0) -> str:
        # TODO add test to this

        tag = self.tag
        attributes = self.attributes

        if len(attributes.keys()) > 0:
            open_tag = f"<{tag}" + " " + as_kwargs(attributes, " ")
        else:
            open_tag = f"<{tag}"

        open_close_tag = open_tag
        open_tag += ">"
        open_close_tag += "/>"

        spacer = " " * indent
        children = [child.render(indent=indent + 4) for child in self]

        if len(children) == 0:
            return f"{spacer}{open_close_tag}"

        return join(
            [f"{spacer}{open_tag}", *children, f"{spacer}</{tag}>"], "\n"
        )
