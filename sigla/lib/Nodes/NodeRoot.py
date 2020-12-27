from sigla.lib.Nodes.Node import Node
from sigla.lib.helpers.Context import Context


class NodeRoot(Node):
    kind = "root"

    def process(self, ctx=None):
        return list(map(lambda e: e.process(ctx), self.children))
