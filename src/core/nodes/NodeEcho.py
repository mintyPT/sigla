from core.nodes.Node import Node
from core.outputs.OutputEcho import OutputEcho


class NodeEcho(Node):
    def process(self):
        super().process()
        content = self.children()
        return OutputEcho(content)
