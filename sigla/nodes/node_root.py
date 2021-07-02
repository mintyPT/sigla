from sigla.nodes.node import Node
from sigla.nodes.abstract_public_node import AbstractPublicNode


class NodeRoot(AbstractPublicNode, Node):
    def process(self):
        super().process()
        for child in self.children:
            child.process()

    def finish(self):
        return [child.finish() for child in self.children]
