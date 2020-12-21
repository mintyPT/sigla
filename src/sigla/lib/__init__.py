from xml.etree import ElementTree as ET

from sigla.lib.Nodes.Node import Node
from sigla.lib.Nodes.NodeFile import FileNode
from sigla.lib.Nodes.NodeRoot import RootNode
from sigla.lib.Nodes.NodeTemplate import TemplateNode


def from_xml(node: ET.Element):
    attributes = Node.attributes_from_node(node)
    meta = Node.meta_from_node(node)

    children = []
    for child in node:
        children.append(from_xml(child))

    if node.tag == 'file':
        return FileNode(children=children, attributes=attributes, meta=meta)
    elif node.tag == 'root':
        return RootNode(children=children, attributes=attributes, meta=meta)
    else:
        return TemplateNode(children=children, attributes=attributes, meta=meta)
