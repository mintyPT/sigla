import unittest

from sigla.nodes.NodeTemplate import NodeTemplate
from sigla import load_node
from sigla.templates.engines import JinjaEngine
from .helpers.node_factory_for_testing import node_factory_for_testing


class TestConvertToInternalClasses(unittest.TestCase):
    def test_simple(self):
        source = "<a name='a'><b name='b'></b></a>"
        got = load_node("xml_string", source, factory=node_factory_for_testing)

        engine = JinjaEngine()
        expected = NodeTemplate("a", engine, attributes={"name": "a"}).append(
            NodeTemplate("b", engine, attributes={"name": "b"})
        )

        self.assertEqual(got, expected)

    def test_conversion(self):
        source = "<a name='a' age-int='33' price-float='1.2' data-json='{\"v1\": 1}' b-bool='True' c-bool='1' d-bool='true' e-bool='ads'></a>"  # noqa: E501
        got = load_node("xml_string", source, factory=node_factory_for_testing)

        expected = {
            "name": "a",
            "age": 33,
            "price": 1.2,
            "data": {"v1": 1},
            "b": True,
            "c": True,
            "d": True,
            "e": False,
        }

        self.assertEqual(got.data.attributes, expected)
