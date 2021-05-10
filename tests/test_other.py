import unittest

from sigla.utils.errors import TemplateDoesNotExistError
from sigla import load_node
from .helpers.node_factory_for_testing import node_factory_for_testing


class TestOther(unittest.TestCase):
    def test_assert_template_does_not_exist(self):
        with self.assertRaises(TemplateDoesNotExistError) as context:
            provided = """<most-random name="core"></most-random>"""
            base = load_node(
                "xml_string", provided, factory=node_factory_for_testing
            )
            base.process()

        self.assertTrue(
            "Missing template most-random" in context.exception.message
        )
