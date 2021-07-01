from sigla.nodes.node import Node
from sigla.nodes import PublicNodeABC


class NodeRoot(PublicNodeABC, Node):
    def process(self):
        super().process()
        for child in self.children:
            child.process()

    def finish(self):
        return [child.finish() for child in self.children]
