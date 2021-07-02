from pathlib import Path

from sigla.nodes.node import Node
from sigla.nodes.abstract_public_node import AbstractPublicNode
from sigla.utils.helpers import ensure_dirs


class NodeFile(AbstractPublicNode, Node):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self.content = None

    @property
    def to(self):
        return self.data.attributes["to"]

    def process(self):
        super().process()

        self.content = self.children()

        self.validate_to_attribute()

        return self

    def validate_to_attribute(self):
        if "to" not in self.data.attributes.keys():
            raise AttributeError(
                "You need to provide the propriety `to` with a filepath on "
                "the element <file> to save the results to"
            )

    def __eq__(self, o: any) -> bool:
        if type(self) == self.__class__ and type(o) == self.__class__:
            if self.content == o.content and self.to == o.path:
                return True
        return False

    def finish(self):
        print(f":: Saving {self.to}")
        ensure_dirs(Path(self.to).parent)
        with open(self.to, "w") as h:
            h.write(self.content)
