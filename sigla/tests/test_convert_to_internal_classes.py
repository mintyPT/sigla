from sigla.lib.funcs import import_from_xml_string
from sigla.classes.nodes.NodeTemplate import NodeTemplate
from sigla.tests.helpers import MemoryNodeTemplate


class TestConvertToInternalClasses:
    def test_simple(self):
        source = "<a name='a'><b name='b'></b></a>"
        got_nodes = NodeTemplate("a", {"name": "a"})
        got_nodes.append(NodeTemplate("b", {"name": "b"}))
        assert (
            import_from_xml_string(source, TemplateClass=MemoryNodeTemplate)
            == got_nodes
        )
