from sigla.nodes.node import Node


class NodeRoot(Node):
    def process(self):
        self._process()
        for child in self.children:
            child.process()

    def finish(self):
        return [child.finish() for child in self.children]
