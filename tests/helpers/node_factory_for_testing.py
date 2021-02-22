from core.nodes.NodeEcho import NodeEcho
from core.nodes.NodeFile import NodeFile
from core.nodes.RootRoot import RootRoot
from tests.helpers.AutoNodeTemplate import AutoNodeTemplate
from core.nodes.Node import Node


def node_factory_for_testing(tag, attributes) -> Node:
    if tag == "root":
        return RootRoot(tag, attributes=attributes)
    elif tag == "file":
        return NodeFile(tag, attributes=attributes)
    elif tag == "echo":
        return NodeEcho(tag, attributes=attributes)
    else:
        return AutoNodeTemplate(tag, attributes=attributes)
