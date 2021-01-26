from sigla.classes.nodes.BaseNode import BaseNode
from sigla.lib.outputs.EchoOutput import EchoOutput


class EchoNode(BaseNode):
    def process(self):
        super().process()
        results = [child.process() for child in self.children]
        content = "\n".join(results)
        return EchoOutput(content)
