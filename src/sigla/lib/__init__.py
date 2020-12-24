from xml.etree import ElementTree as ET

from sigla.lib.Nodes.Node import Node
from sigla.lib.Nodes.NodeFile import NodeFile
from sigla.lib.Nodes.NodeRoot import NodeRoot
from sigla.lib.Nodes.NodeTemplate import NodeTemplate


def from_xml(node: ET.Element):
    attributes = Node.attributes_from_node(node)
    meta = Node.meta_from_node(node)

    children = []
    for child in node:
        children.append(from_xml(child))

    if node.tag == "file":
        return NodeFile(children=children, attributes=attributes, meta=meta)
    elif node.tag == "root":
        return NodeRoot(children=children, attributes=attributes, meta=meta)
    else:
        return NodeTemplate(
            children=children, attributes=attributes, meta=meta
        )
