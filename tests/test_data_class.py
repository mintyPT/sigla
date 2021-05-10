import unittest
from sigla.data.Data import Data
from sigla.data.loaders import data_from_xml_string


class TestDataClass(unittest.TestCase):
    def test_load_single_node(self):
        expected = Data(tag="a", attributes={"name": "your_name"})
        self.assertEqual(
            data_from_xml_string("<a name='your_name' />"),
            expected,
        )

    def test_nested_nodes(self):
        expected = Data(tag="a", attributes={"name": "a"}, children=[(Data("b", {"name": "b"}))])
        self.assertEqual(
            data_from_xml_string("<a name='a'><b name='b'></b></a>"),
            expected,
        )
