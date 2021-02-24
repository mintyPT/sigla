from sigla.core.outputs.OutputEcho import OutputEcho
from sigla.utils import import_node

Node = import_node()


class NodeEcho(Node):
    def process(self):
        super().process()
        content = self.children()
        return OutputEcho(content)
