import unittest

from sigla.nodes.Node import Node


class TestNode(unittest.TestCase):
    def test_empty_attributes(self):
        node = Node("any")
        self.assertEqual(node.attributes, {})

    def test_basic_attr(self):
        node = Node("any", attributes={"name": "mg", "age": 33})

        self.assertEqual(node.attributes["name"], "mg")
        self.assertEqual(node.name, "mg")

        kwargs = node.attributes.as_kwargs(sep=None)
        self.assertIn("age=33", kwargs)
        self.assertEqual(len(node.children(sep=None)), 0)
