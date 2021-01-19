from textwrap import dedent

from sigla.lib2.ImportNode import ImportNode
from sigla.lib2.node.NodeTemplate import NodeTemplate


class MemoryNodeTemplate(NodeTemplate):
    def raw_template_loader(self, tag):
        if tag == 'b':
            return '{{ name }}-{{ age }}'
        if tag == 'person':
            return dedent('''
            ---
            second_name: "santos"
            ---
            {{- name }}-{{ second_name }}-{{ age }}
            ''')
        if tag == 'a':
            return '-a-{{ render(children) }}-a-'
        if tag == 'a2':
            return '-a-{% for child in children %}{{ render(child) }}{% endfor %}-a-'
        if tag == 'ta':
            return '{{ render(children) }}'
        if tag == 'tb':
            return '{{ render(children) }}'
        if tag == 'tc':
            return '{{ ra }}{{ rb }}{{ name }}'
        raise NotImplementedError(f"Missing memory template for {tag}")


def from_nodes_to_internal_memory(node: ImportNode, context=None):
    child_nodes = [from_nodes_to_internal_memory(r) for r in node.children]

    ret = MemoryNodeTemplate(
        node.tag,
        attributes=node.attributes,
    )

    for node in child_nodes:
        ret.append(node)

    return ret