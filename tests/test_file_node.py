import unittest
from sigla.nodes.node_file import NodeFile
from sigla.templates.engines import JinjaEngine


class TestFileNode(unittest.TestCase):
    def test_empty_attributes(self):
        engine = JinjaEngine()
        node = NodeFile("any", engine)

        with self.assertRaises(AttributeError):
            node.process()
