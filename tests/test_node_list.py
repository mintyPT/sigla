import unittest

from sigla import config
from sigla.nodes.node_list import NodeList
from sigla.nodes.node_root import NodeRoot
from sigla.templates.engines import JinjaEngine
from sigla.templates.loaders import FileTemplateLoader


class TestNodeList(unittest.TestCase):
    def test_filter(self):
        engine = JinjaEngine()
        loader = FileTemplateLoader(config.path.templates, "jinja2")
        node_list = NodeList(
            [
                NodeRoot(s, engine, loader)
                for s in ["cenas", "cenas", "cenas2", "cenas3"]
            ]
        )

        filtered = node_list.filter(tag="cenas")
        self.assertEqual(len(filtered), 2, "Should have 2 elements")

        el = filtered.first()
        self.assertEqual(
            type(el), NodeRoot, "Should fetch one element and be of type Node"
        )

        filtered = node_list.filter(tag="cenas2")
        self.assertEqual(len(filtered), 1, "Should have 1 elements")
