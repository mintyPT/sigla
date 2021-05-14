import pathlib
import unittest
from sigla.nodes.Node import Node
from sigla.nodes.NodeRoot import NodeRoot
from sigla.templates.engines import JinjaEngine


class BaseNode(Node):
    scripts_base_path = pathlib.Path(__file__).parent.joinpath("scripts")


class TestNode(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.engine = JinjaEngine()

    def test_empty_attributes(self):
        node = NodeRoot("any", self.engine)
        self.assertEqual(node.attributes, {})

    def test_script(self):
        node = BaseNode("any", self.engine, attributes={"script": "hello.py"})
        self.assertEqual(node.attributes.get("name"), "mauro")

    def test_basic_attr(self):
        node = NodeRoot("any", self.engine, attributes={"name": "mg", "age": 33})

        self.assertEqual(node.attributes["name"], "mg")
        self.assertEqual(node.name, "mg")

        kwargs = node.attributes.as_kwargs(sep=None)
        self.assertIn("age=33", kwargs)
        self.assertEqual(len(node.children(sep=None)), 0)

    def test_replacement_in_props(self):
        node = NodeRoot("any", self.engine, attributes={"name": "mg", "path": "{{name}}-"})
        node.process()
        self.assertEqual(node.attributes["path"], "mg-")

    def test_replacement_in_props_of_children(self):
        node_child = NodeRoot("child", self.engine, attributes={"path": "{{name}}-"})
        node = NodeRoot(
            "root", self.engine, attributes={"name": "mg"}, children=[node_child]
        )

        node.process()
        self.assertEqual(node.children.first().attributes["path"], "mg-")
