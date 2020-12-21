from xml.etree import ElementTree as ET

from sigla.lib.Node import Node
from sigla.lib.NodeFile import FileNode
from sigla.lib.NodeRoot import RootNode
from sigla.lib.NodeTemplate import TemplateNode


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
