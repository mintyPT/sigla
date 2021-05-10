import unittest
from sigla.nodes.NodeFile import NodeFile


class TestFileNode(unittest.TestCase):
    def test_empty_attributes(self):
        node = NodeFile("any")

        with self.assertRaises(AttributeError):
            node.process()
