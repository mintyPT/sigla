from .helpers.node_factory_for_testing import node_factory_for_testing
from core.errors import TemplateDoesNotExistError
from core.importers import base_node_to_node, string_to_nodes


class TestOther:
    def test_assert_template_does_not_exist(self):
        ok = False
        try:
            provided = """<most-random name="core"></most-random>"""
            base = base_node_to_node(
                string_to_nodes(provided),
                factory=node_factory_for_testing,
            )
            base()
        except TemplateDoesNotExistError as e:
            ok = True
            assert e.message == "Missing template most-random"

        assert ok, "Expected an exception due to missing template"
