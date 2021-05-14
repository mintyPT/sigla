from sigla.nodes.NodeEcho import NodeEcho
from sigla.nodes.NodeFile import NodeFile
from sigla.nodes.NodeRoot import NodeRoot
from sigla.nodes.NodeTemplate import NodeTemplate
from sigla.templates.engines import JinjaEngine


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

        engine = JinjaEngine()

        if node_creator:
            return node_creator(tag, engine, attributes=attributes)
        else:
            return default_creator(tag, engine, attributes=attributes)
