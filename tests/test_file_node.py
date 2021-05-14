import unittest
from sigla.nodes.NodeFile import NodeFile
from sigla.templates.engines import JinjaEngine


class TestFileNode(unittest.TestCase):
    def test_empty_attributes(self):
        node = NodeFile("any", JinjaEngine())

        with self.assertRaises(AttributeError):
            node.process()
