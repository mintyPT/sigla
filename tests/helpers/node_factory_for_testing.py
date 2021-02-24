from sigla.core.nodes.NodeEcho import NodeEcho
from sigla.core.nodes.NodeFile import NodeFile
from sigla.core.nodes.NodeRoot import NodeRoot
from sigla.types import NodeType
from tests.helpers.AutoNodeTemplate import AutoNodeTemplate


def node_factory_for_testing(tag, attributes) -> NodeType:
    if tag == "root":
        return NodeRoot(tag, attributes=attributes)
    elif tag == "file":
        return NodeFile(tag, attributes=attributes)
    elif tag == "echo":
        return NodeEcho(tag, attributes=attributes)
    else:
        return AutoNodeTemplate(tag, attributes=attributes)
