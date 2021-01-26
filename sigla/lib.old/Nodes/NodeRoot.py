from sigla.lib.Nodes.Node import Node
from sigla.lib.helpers.Context import Context


class NodeRoot(Node):
    kind = "root"

    def process(self, ctx=None):

        if ctx is None:
            ctx = Context()
        ctx.push_context(self)

        return list(map(lambda e: e.process(ctx), self.children))
