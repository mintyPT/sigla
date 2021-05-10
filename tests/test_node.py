import unittest

from sigla.nodes.NodeRoot import NodeRoot


class TestNode(unittest.TestCase):
    def test_empty_attributes(self):
        node = NodeRoot("any")
        self.assertEqual(node.attributes, {})

    def test_basic_attr(self):
        node = NodeRoot("any", attributes={"name": "mg", "age": 33})

        self.assertEqual(node.attributes["name"], "mg")
        self.assertEqual(node.name, "mg")

        kwargs = node.attributes.as_kwargs(sep=None)
        self.assertIn("age=33", kwargs)
        self.assertEqual(len(node.children(sep=None)), 0)
