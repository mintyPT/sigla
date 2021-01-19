from sigla.lib2.helpers.ImportNode import ImportNode
from sigla.lib2.nodes.BaseNode import BaseNode
from sigla.lib2.nodes.NodeTemplate import NodeTemplate


def from_import_node_to_base_node(node: ImportNode) -> BaseNode:
    child_nodes = [from_import_node_to_base_node(r) for r in node.children]

    ret = NodeTemplate(
        node.tag,
        attributes=node.attributes,
    )

    for node in child_nodes:
        ret.append(node)

    return ret
