from sigla.lib2.nodes.BaseNode import BaseNode
from sigla.lib2.outputs.FileOutput import FileOutput


class FileNode(BaseNode):
    def process(self):
        super().process()
        results = [child.process() for child in self.children]
        content = "\n".join(results)
        if "to" not in self.attributes.keys():
            raise Exception(
                "You need to provide the propriety `to` with a filepath on the element <file> to save the results to"
            )
        to = self.attributes["to"]

        return FileOutput(to, content)