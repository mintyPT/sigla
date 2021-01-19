from sigla.lib2.importers.xml import load_xml
from sigla.tests.helpers import (
    MemoryNodeTemplate,
    from_nodes_to_internal_memory,
)


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
        got = from_nodes_to_internal_memory(load_xml(provided)).process()

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
        got = from_nodes_to_internal_memory(load_xml(provided)).process()
        expected = "one/two/three"

        assert got == expected
