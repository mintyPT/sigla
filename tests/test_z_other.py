from sigla.errors import TemplateDoesNotExistError
from sigla.sigla import string_to_data, data_to_node
from .helpers.node_factory_for_testing import node_factory_for_testing


class TestOther:
    def test_assert_template_does_not_exist(self):
        ok = False
        try:
            provided = """<most-random name="core"></most-random>"""
            base = data_to_node(
                string_to_data(provided),
                factory=node_factory_for_testing,
            )
            base()
        except TemplateDoesNotExistError as e:
            ok = True
            assert e.message == "Missing template most-random"

        assert ok, "Expected an exception due to missing template"
