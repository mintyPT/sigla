from sigla.lib2.nodes.BaseNode import BaseNode
from sigla.lib2.outputs.EchoOutput import EchoOutput


class EchoNode(BaseNode):
    def process(self):
        super().process()
        results = [child.process() for child in self.children]
        content = "\n".join(results)
        return EchoOutput(content)
