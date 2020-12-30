__version__ = "0.0.40"

from sigla.lib import from_xml


def process_node(root, filters=None):
    if filters is None:
        filters = {}

    node = from_xml(root, filters=filters)
    node.process()
