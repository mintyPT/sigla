from sigla.lib.Node import Node
from sigla.lib.helpers.Context import Context


class RootNode(Node):
    def process(self, ctx):
        if ctx is None:
            ctx = Context()
        return list(map(lambda e: e.process(ctx), self.children))