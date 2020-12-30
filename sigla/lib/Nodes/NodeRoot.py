from sigla.lib.Nodes.Node import Node


class NodeRoot(Node):
    kind = "root"

    def process(self, ctx=None):
        return list(map(lambda e: e.process(ctx), self.children))
