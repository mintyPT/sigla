__version__ = "0.0.31"

from sigla.lib import from_xml


def process_node(root):
    node = from_xml(root)
    node.process()
