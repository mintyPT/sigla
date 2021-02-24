from sigla.core.outputs.OutputFile import OutputFile
from sigla.utils import import_node

Node = import_node()


class NodeFile(Node):
    def process(self):
        super().process()
        content = self.children()
        if "to" not in self.data.attributes.keys():
            raise AttributeError(
                "You need to provide the propriety `to` with a filepath on the element <file> to save the results to"  # noqa
            )
        to = self.data.attributes["to"]

        return OutputFile(to, content)
