from sigla.lib2.funcs import from_import_node_to_base_node
from sigla.lib2.importers.xml import load_xml
from sigla.tests.helpers import MemoryNodeTemplate


class TestRendering:
    def test_simple(self):
        node = MemoryNodeTemplate("b", {"name": "minty", "age": "33"})
        got = node.process()
        expected = "minty-33"
        assert got == expected

    def test_simple_with_frontmatter(self):
        provided = """
        <person name="minty" age="33" />
        """
        got = from_import_node_to_base_node(
            load_xml(provided), TemplateClass=MemoryNodeTemplate
        ).process()

        expected = "minty-santos-33"
        assert got == expected

    def test_render_child(self):
        expected = "-a-minty-33-a-"
        node = MemoryNodeTemplate("a", {})
        node.append(MemoryNodeTemplate("b", {"name": "minty", "age": "33"}))
        got = node.process()
        assert got == expected

        expected = "-a-minty-33-a-"
        node.tag = "a2"
        got = node.process()
        assert got == expected

    def test_render_context2(self):
        provided = """
        <ta ra="one/">
            <tb name="ttbb" rb="two/">
                <tc name="three" />
            </tb>
        </ta>
        """
        got = from_import_node_to_base_node(
            load_xml(provided), TemplateClass=MemoryNodeTemplate
        ).process()
        expected = "one/two/three"

        assert got == expected

    def test_fm_child(self):
        provided = """
        <first-level>
            <second-level>
                <third-level>
                </third-level>
            </second-level>
        </first-level>
        """
        got = from_import_node_to_base_node(
            load_xml(provided), TemplateClass=MemoryNodeTemplate
        ).process()
        expected = "__one/two/three__"

        assert got == expected
