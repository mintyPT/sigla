from sigla.lib2.errors import TemplateDoesNotExistError
from sigla.lib2.funcs import from_import_node_to_base_node
from sigla.lib2.importers.xml import load_xml
from sigla.tests.helpers import MemoryNodeTemplate


class TestOther:
    def test_assert_template_does_not_exist(self):
        ok = False
        try:
            provided = """<most-random name="sigla"></most-random>"""
            from_import_node_to_base_node(
                load_xml(provided), TemplateClass=MemoryNodeTemplate
            ).process()
        except TemplateDoesNotExistError as e:
            ok = True
            assert e.message == "Missing template most-random"
            data = e.from_entity.get_data_for_template()
            assert data["name"] == "sigla"

        assert ok, "Expected an exception due to missing template"
