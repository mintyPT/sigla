from sigla.lib2.nodes.BaseNode import BaseNode


class RootNode(BaseNode):
    def process(self):
        super().process()
        return [child.process() for child in self.children]
