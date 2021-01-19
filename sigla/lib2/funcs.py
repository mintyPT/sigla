from sigla.lib2.ImportNode import ImportNode
from sigla.lib2.node.BaseNode import BaseNode
from sigla.lib2.node.NodeTemplate import NodeTemplate


def from_nodes_to_internal(node: ImportNode) -> BaseNode:
    child_nodes = [from_nodes_to_internal(r) for r in node.children]

    ret = NodeTemplate(
        node.tag,
        attributes=node.attributes,
    )

    for node in child_nodes:
        ret.append(node)

    return ret
