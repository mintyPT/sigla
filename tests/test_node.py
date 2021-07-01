import pathlib
import unittest

from sigla import config
from sigla.nodes.node import Node
from sigla.nodes.node_root import NodeRoot
from sigla.templates.engines import JinjaEngine
from sigla.templates.loaders import FileTemplateLoader


class BaseNode(Node):
    scripts_base_path = pathlib.Path(__file__).parent.joinpath("scripts")


class TestNode(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.engine = JinjaEngine()
        self.loader = FileTemplateLoader(config.path.templates, "jinja2")

    def test_empty_attributes(self):
        node = NodeRoot("any", self.engine, self.loader)
        self.assertEqual(node.attributes, {})

    def test_script(self):
        node = BaseNode(
            "any", self.engine, self.loader, attributes={"script": "hello.py"}
        )
        self.assertEqual(node.attributes.get("name"), "mauro")

    def test_basic_attr(self):
        node = NodeRoot(
            "any",
            self.engine,
            self.loader,
            attributes={"name": "mg", "age": 33},
        )

        self.assertEqual(node.attributes["name"], "mg")
        self.assertEqual(node.name, "mg")

        kwargs = node.attributes.as_kwargs(sep=None)
        self.assertIn("age=33", kwargs)
        self.assertEqual(len(node.children(sep=None)), 0)

    def test_replacement_in_props(self):
        node = NodeRoot(
            "any",
            self.engine,
            self.loader,
            attributes={"name": "mg", "path": "{{name}}-"},
        )
        node.process()
        self.assertEqual(node.attributes["path"], "mg-")

    def test_replacement_in_props_of_children(self):
        node_child = NodeRoot(
            "child", self.engine, self.loader, attributes={"path": "{{name}}-"}
        )
        node = NodeRoot(
            "root",
            self.engine,
            self.loader,
            attributes={"name": "mg"},
            children=[node_child],
        )

        node.process()
        self.assertEqual(node.children.first().attributes["path"], "mg-")
