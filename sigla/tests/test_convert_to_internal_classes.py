from sigla.lib2.importers.xml import import_from_xml_string
from sigla.lib2.nodes.NodeTemplate import NodeTemplate


class TestConvertToInternalClasses:
    def test_simple(self):
        source = "<a name='a'><b name='b'></b></a>"
        got_nodes = NodeTemplate('a', {"name": "a"})
        got_nodes.append(NodeTemplate('b', {"name": "b"}))
        assert import_from_xml_string(source) == got_nodes