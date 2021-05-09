from pathlib import Path

from sigla.nodes.Node import Node
from sigla.utils.helpers import ensure_dirs


class NodeFile(Node):
    def __init__(self, tag, attributes=None):
        super().__init__(tag, attributes)
        self.content = None
        self.to = None

    def process(self):
        super().process()

        self.content = self.children()

        if "to" not in self.data.attributes.keys():
            self.raise_missing_to_attribute()

        self.to = self.data.attributes["to"]

        return self

    def raise_missing_to_attribute(self):
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
