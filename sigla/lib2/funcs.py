from sigla.lib2.helpers.ImportNode import ImportNode
from sigla.lib2.importers.xml import load_xml
from sigla.lib2.nodes.BaseNode import BaseNode
from sigla.lib2.nodes.EchoNode import EchoNode
from sigla.lib2.nodes.NodeTemplate import NodeTemplate
from sigla.lib2.nodes.RootNode import RootNode
from sigla.lib2.nodes.FileNode import FileNode


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
        load_xml(source),
        TemplateClass=TemplateClass,
        RootClass=RootClass,
        FileClass=FileClass,
        EchoClass=EchoClass,
    )
