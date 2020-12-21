__version__ = "0.0.11"


from sigla.lib.Node import Node
from sigla.lib import from_xml
from sigla.lib.helpers.misc import cast_array


def process_node(root):
    node = from_xml(root)
    node.process()
