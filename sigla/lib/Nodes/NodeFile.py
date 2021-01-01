import os
from pathlib import Path

from sigla.lib.Nodes.Node import Node
from sigla.lib.helpers.files import ensure_parent_dir
from sigla.lib.helpers.Context import Context


class NodeFile(Node):
    kind = "file"

    def process(self, ctx=None):
        if ctx is None:
            ctx = Context()

        if not self.name:
            raise Exception("# No name attached to the file element.")

        ctx.push_context(self)

        text = ""
        for child in self:
            text += child.process(ctx)

        ctx.pop_context()

        filepath = Path.cwd().joinpath(self.name)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(text)
