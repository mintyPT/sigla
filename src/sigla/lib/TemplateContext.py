from typing import List, Dict
from sigla.lib.Node import Node


class TemplateContext:
    node_stack: List[Node] = []
    context_stack: List[Dict] = []

    def get_context(self):
        arr = self.context_stack

        result = {}
        for obj in arr:
            for k, v in obj.items():
                result[k] = v
        return result

    def push_context(self, node: Node):
        self.node_stack.append(node)
        self.context_stack.append(node.attributes)
        return self.get_context()

    def pop_context(self):
        self.node_stack.pop()
        return self.context_stack.pop()