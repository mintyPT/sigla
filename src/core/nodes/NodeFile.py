from core.nodes.Node import Node
from core.outputs.OutputFile import OutputFile


class NodeFile(Node):
    def process(self):
        super().process()
        content = self.children()
        if "to" not in self.data.attributes.keys():
            raise Exception(
                "You need to provide the propriety `to` with a filepath on the element <file> to save the results to"  # noqa
            )
        to = self.data.attributes["to"]

        return OutputFile(to, content)
