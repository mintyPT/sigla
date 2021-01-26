from xml.etree import ElementTree as ET
from sigla.lib.helpers.ImportNode import ImportNode


def load_xml(s) -> ImportNode:
    obj: ET = ET.fromstring(s)
    node = process_xml(obj)
    return node


def process_xml(obj) -> ImportNode:
    node = ImportNode(obj.tag, attributes=obj.attrib.copy(), children=[])
    for child in obj:
        node.children.append(process_xml(child))
    return node
