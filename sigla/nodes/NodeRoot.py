from sigla.nodes.Node import Node
from sigla.nodes.NodeABC import PublicNodeABC


class NodeRoot(PublicNodeABC, Node):
    def process(self):
        super().process()
        for child in self.children:
            child.process()

    def finish(self):
        return [child.finish() for child in self.children]
