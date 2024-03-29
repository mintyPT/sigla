import unittest

from sigla.nodes.node_template import NodeTemplate
from sigla import load_node, config
from sigla.templates.engines import JinjaEngine
from sigla.templates.loaders import FileTemplateLoader
from tests.helpers.node_factory_for_testing import node_factory_for_testing


class TestConvertToInternalClasses(unittest.TestCase):
    def test_simple(self):
        source = "<a name='a'><b name='b'></b></a>"
        got = load_node("xml", source, factory=node_factory_for_testing)

        loader = FileTemplateLoader(config.path.templates, "jinja2")
        engine = JinjaEngine()
        expected = NodeTemplate(
            "a", engine, loader, attributes={"name": "a"}
        ).append(NodeTemplate("b", engine, loader, attributes={"name": "b"}))

        self.assertEqual(got, expected)

    def test_conversion(self):
        source = "<a name='a' age-int='33' price-float='1.2' data-json='{\"v1\": 1}' b-bool='True' c-bool='1' d-bool='true' e-bool='ads'></a>"  # noqa: E501
        got = load_node("xml", source, factory=node_factory_for_testing)

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
