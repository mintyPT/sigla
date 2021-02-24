from sigla.utils import import_node

Node = import_node()


class NodeRoot(Node):
    def process(self):
        super().process()
        return [child() for child in self.children]
