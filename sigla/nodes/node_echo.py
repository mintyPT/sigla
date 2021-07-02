from sigla.nodes.node import Node
from sigla.nodes.abstract_public_node import AbstractPublicNode


class NodeEcho(AbstractPublicNode, Node):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self.content = None

    def process(self):
        super().process()
        self.content = self.children()
        return self

    def __eq__(self, o: any) -> bool:
        if type(self) == self.__class__ and type(o) == self.__class__:
            if self.content == o.content:
                return True
        return False

    def finish(self):
        print(self.content)
