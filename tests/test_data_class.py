import unittest
from sigla.data.data import Data
from sigla.data.loaders import XMLStringDataLoader


class TestDataClass(unittest.TestCase):
    def test_load_single_node(self):
        expected = Data(tag="a", attributes={"name": "your_name"})
        self.assertEqual(
            XMLStringDataLoader("<a name='your_name' />").load(),
            expected,
        )

    def test_nested_nodes(self):
        expected = Data(
            tag="a",
            attributes={"name": "a"},
            children=[(Data("b", {"name": "b"}))],
        )
        self.assertEqual(
            XMLStringDataLoader("<a name='a'><b name='b'></b></a>").load(),
            expected,
        )
