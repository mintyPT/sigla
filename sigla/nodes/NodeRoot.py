from sigla.nodes.Node import Node


class NodeRoot(Node):
    def process(self):
        super().process()
        return [child() for child in self.children]
