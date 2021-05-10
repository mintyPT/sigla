from sigla.nodes.Node import Node
from sigla.nodes.NodeABC import PublicNodeABC


class NodeEcho(PublicNodeABC, Node):
    def __init__(self, tag, attributes=None):
        super().__init__(tag, attributes)
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
