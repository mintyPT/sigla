import unittest

from sigla.config import config


class TestCliConfig(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(config.path.root_directory, ".sigla")
        self.assertEqual(config.path.templates, ".sigla/templates")
        self.assertEqual(config.path.snapshots, ".sigla/snapshots")
        self.assertEqual(config.path.definitions, ".sigla/definitions")
        self.assertEqual(config.path.filters, ".sigla/filters.py")

        self.assertEqual(
            config.cls.node_list, "sigla.core.node_lists.NodeList"
        )
        self.assertEqual(config.cls.node, "sigla.core.nodes.Node")
