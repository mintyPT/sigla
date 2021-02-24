from sigla import from_xml_string
from sigla.core.nodes.NodeTemplate import NodeTemplate
from .helpers.node_factory_for_testing import node_factory_for_testing


class TestConvertToInternalClasses:
    def test_simple(self):
        source = "<a name='a'><b name='b'></b></a>"
        got = from_xml_string(source, factory=node_factory_for_testing)

        expected = NodeTemplate("a", {"name": "a"}).append(
            NodeTemplate("b", {"name": "b"})
        )

        assert got == expected

    def test_conversion(self):
        source = "<a name='a' age-int='33' price-float='1.2' data-json='{\"v1\": 1}' b-bool='True' c-bool='1' d-bool='true' e-bool='ads'></a>"  # noqa: E501
        got = from_xml_string(source, factory=node_factory_for_testing)

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

        assert got.data.attributes == expected
