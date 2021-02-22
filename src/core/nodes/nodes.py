from core.nodes.NodeEcho import NodeEcho
from core.nodes.NodeFile import NodeFile
from core.nodes.NodeTemplate import NodeTemplate
from core.nodes.RootRoot import RootRoot
from core.nodes.Node import Node


def node_factory(tag, attributes) -> Node:
    if tag == "root":
        return RootRoot(tag, attributes=attributes)
    elif tag == "file":
        return NodeFile(tag, attributes=attributes)
    elif tag == "echo":
        return NodeEcho(tag, attributes=attributes)
    else:
        return NodeTemplate(tag, attributes=attributes)
