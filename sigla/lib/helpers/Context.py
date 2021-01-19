from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from sigla.lib.Nodes.Node import Node


class Context:
    node_stack: List["ImportNode"] = []
    context_stack: List[Dict] = []

    def get_context(self):
        return self.merge_contexts(self.context_stack)

    def merge_contexts(self, arr):
        result = {}
        for obj in arr:
            for k, v in obj.items():
                result[k] = v
        return result

    def push_context(self, node: "ImportNode"):
        self.node_stack.append(node)
        self.context_stack.append(node.attributes)
        return self.get_context()

    def pop_context(self):
        self.node_stack.pop()
        return self.context_stack.pop()

    def get_last_context(self):
        return self.merge_contexts(self.context_stack[-1:])
