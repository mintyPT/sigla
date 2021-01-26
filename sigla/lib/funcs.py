from sigla.classes.ImportNode import ImportNode
from sigla.helpers.xml import load_xml_string_into_nodes
from sigla.lib.nodes.BaseNode import BaseNode
from sigla.lib.nodes.EchoNode import EchoNode
from sigla.lib.nodes.NodeTemplate import NodeTemplate
from sigla.lib.nodes.RootNode import RootNode
from sigla.lib.nodes.FileNode import FileNode


def from_import_node_to_base_node(
    node: ImportNode,
    TemplateClass=NodeTemplate,
    RootClass=RootNode,
    FileClass=FileNode,
    EchoClass=EchoNode,
) -> BaseNode:
    child_nodes = [
        from_import_node_to_base_node(r, TemplateClass=TemplateClass)
        for r in node.children
    ]

    if node.tag == "root":
        ret = RootClass(
            node.tag,
            attributes=node.attributes,
        )
    elif node.tag == "file":
        ret = FileClass(
            node.tag,
            attributes=node.attributes,
        )
    elif node.tag == "echo":
        ret = EchoClass(
            node.tag,
            attributes=node.attributes,
        )
    else:
        ret = TemplateClass(
            node.tag,
            attributes=node.attributes,
        )

    for node in child_nodes:
        ret.append(node)

    return ret


def import_from_xml_string(
    source,
    TemplateClass=NodeTemplate,
    RootClass=RootNode,
    FileClass=FileNode,
    EchoClass=EchoNode,
):
    return from_import_node_to_base_node(
        load_xml_string_into_nodes(source),
        TemplateClass=TemplateClass,
        RootClass=RootClass,
        FileClass=FileClass,
        EchoClass=EchoClass,
    )
