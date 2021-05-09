import unittest

from sigla.nodes.Node import Node
from sigla.nodes.NodeList import NodeList


class TestNodeList(unittest.TestCase):
    def test_filter(self):
        node_list = NodeList(
            [Node(s) for s in ["cenas", "cenas", "cenas2", "cenas3"]]
        )

        filtered = node_list.filter(tag="cenas")
        self.assertEqual(len(filtered), 2, "Should have 2 elements")

        el = filtered.first()
        self.assertEqual(
            type(el), Node, "Should fetch one element and be of type Node"
        )

        filtered = node_list.filter(tag="cenas2")
        self.assertEqual(len(filtered), 1, "Should have 1 elements")
