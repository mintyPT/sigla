from core.nodes.Node import Node


class RootRoot(Node):
    def process(self):
        super().process()
        return [child() for child in self.children]
