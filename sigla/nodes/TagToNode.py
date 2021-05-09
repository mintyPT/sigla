from sigla.nodes.NodeEcho import NodeEcho
from sigla.nodes.NodeFile import NodeFile
from sigla.nodes.NodeRoot import NodeRoot
from sigla.nodes.NodeTemplate import NodeTemplate


class TagToNode:
    default = NodeTemplate
    reference = {
        "root": NodeRoot,
        "file": NodeFile,
        "echo": NodeEcho,
    }

    def __call__(self, tag: str, attributes: object):
        node_creator = self.reference.get(tag)
        default_creator = self.default

        if node_creator:
            return node_creator(tag, attributes=attributes)
        else:
            return default_creator(tag, attributes=attributes)
