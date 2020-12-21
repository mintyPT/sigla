__version__ = "0.0.11"


from sigla.lib.Node import Node
from sigla.lib.Processor import Processor
from sigla.lib.helpers.misc import cast_array


def process_node(root):
    node = Node.from_xml(root)

    processor = Processor()
    result = processor.process_node(node)
    result = cast_array(result)
    return result
