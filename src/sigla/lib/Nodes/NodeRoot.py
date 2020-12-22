from src.sigla.lib.Nodes.Node import Node
from src.sigla.lib.helpers.Context import Context


class NodeRoot(Node):
    def process(self, ctx=None):
        if ctx is None:
            ctx = Context()
        return list(map(lambda e: e.process(ctx), self.children))