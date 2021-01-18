import logging
from dataclasses import dataclass, replace, make_dataclass
from pprint import pprint
from textwrap import dedent
import xml.etree.ElementTree as ET
from typing import List, Type, Union
from jinja2 import Environment, BaseLoader

from sigla.lib.Nodes.template.engines.jinja import jinja


@dataclass
class Node:
    tag: str
    attributes: dict
    children: List['Node']


def load_xml(s):
    obj: ET = ET.fromstring(s)
    node = process_xml(obj)
    return node


def process_xml(obj):
    node = Node(obj.tag, attributes=obj.attrib.copy(), children=[])
    for child in obj:
        node.children.append(process_xml(child))
    return node


class TestXMLLoadingSimple:
    def test_one_element(self):
        node = Node('a', {"name": "myname"}, [])
        assert load_xml(dedent("""<a name="myname" />""")) == node

    def test_two_elements(self):
        nodes = Node('a', {"name": "a"}, [(Node('b', {"name": "b"}, []))])
        input = "<a name='a'><b name='b'></b></a>"
        assert load_xml(input) == nodes


#
class BaseNode:
    tag: str
    attributes: dict
    children: List['BaseNode']
    context: dict

    def __init__(self, tag, attributes=None, children=None, context=None):

        if children is None:
            children = []
        if attributes is None:
            attributes = {}
        if context is None:
            context = {}
        self.tag = tag
        self.attributes = attributes
        self.children = children
        self.context = context.copy()

    def __eq__(self, other):
        return self.tag == other.tag and self.attributes == other.attributes and self.children == other.children  # and self.context == other.context

    def append(self, node: "BaseNode"):
        self.children.append(node)
        context = self.context.copy()
        context.update(self.attributes)
        node.context = context

    def process(self):
        raise NotImplementedError("Please implement process")


class NodeTemplate(BaseNode):

    def process(self):

        def internal_render_method(something: Union[NodeTemplate, List[NodeTemplate]], sep=''):
            if isinstance(something, BaseNode):
                return something.process()
            else:
                return sep.join([node.process() for node in something])

        # def render(self, template, ctx: Context, **kwargs):
        #
        #     if ctx is None:
        #         ctx = Context()
        #
        #     context = ctx.get_context()
        #     last_context = ctx.get_last_context()
        #
        #     data = {}
        #     data.update(last_context)
        #     data.update(kwargs)
        #
        #     result = jinja(
        #         template,
        #         **data,
        #         filters=self.filters,
        #         context=last_context,
        #         all_context=context,
        #         children=self.children,
        #     )
        #
        #     return result

        str_tpl = self.template_loader(self.tag)

        data = self.context.copy()
        data.update(self.attributes)

        return self.render(
            str_tpl,
            **data,
            meta=self.attributes,  # self
            children=self.children,
            render=internal_render_method,
        )

    def template_loader(self, tag) -> str:
        raise NotImplementedError("Please implement template_loader")

    def render(self, tpl, **kwargs) -> str:
        template = Environment(loader=BaseLoader).from_string(tpl)
        return template.render(**kwargs)
    #
    # def __repr__(self) -> str:
    #     return self.process()
    #


def from_nodes_to_internal(node: Node, context=None):
    if context is None:
        context = {"ping": "pong"}
    child_context = context.copy()
    child_context.update(node.attributes.copy())

    ret = NodeTemplate(
        node.tag,
        attributes=node.attributes,
        children=[],
        context=context.copy()
    )

    for r in node.children:
        node = from_nodes_to_internal(r)
        ret.append(node)

    return ret


class TestConvertToInternalClasses:
    def test_simple(self):
        str_input = "<a name='a'><b name='b'></b></a>"
        got_nodes = NodeTemplate('a', {"name": "a"}, [
            NodeTemplate('b', {"name": "b"}, [])
        ])

        assert from_nodes_to_internal(load_xml(str_input)) == got_nodes


class MemoryNodeTemplate(NodeTemplate):
    def template_loader(self, tag):
        if tag == 'b':
            return '{{ name }}-{{ age }}'
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


class TestRendering:
    def test_simple(self):
        node = MemoryNodeTemplate('b', {"name": "minty", "age": "33"}, [])
        got = node.process()
        expected = "minty-33"
        assert got == expected

    def test_render_child(self):
        expected = "-a-minty-33-a-"
        node = MemoryNodeTemplate('a', {}, [
            MemoryNodeTemplate('b', {"name": "minty", "age": "33"}, [])
        ])
        got = node.process()
        assert got == expected

        expected = "-a-minty-33-a-"
        node.tag = 'a2'
        got = node.process()
        assert got == expected

    def test_render_context(self):
        node_a = MemoryNodeTemplate('ta', {"ra": "-ra-"}, [])
        node_b = MemoryNodeTemplate('tb', {"name": "ttbb", "rb": '-rb-'}, [])
        node_c = MemoryNodeTemplate('tc', {"name": "ttcc"}, [])

        node_a.append(node_b)
        node_b.append(node_c)

        got = node_a.process()
        expected = '-ra--rb-ttcc'

        assert got == expected
