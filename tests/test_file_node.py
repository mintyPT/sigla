import unittest

from sigla import config
from sigla.nodes.NodeFile import NodeFile
from sigla.templates.engines import JinjaEngine
from sigla.templates.loaders import FileTemplateLoader


class TestFileNode(unittest.TestCase):
    def test_empty_attributes(self):
        engine = JinjaEngine()
        loader = FileTemplateLoader(config.path.templates, "jinja2")
        node = NodeFile("any", engine, loader)

        with self.assertRaises(AttributeError):
            node.process()
