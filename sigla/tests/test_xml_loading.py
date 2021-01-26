from textwrap import dedent

from sigla.classes.ImportNode import ImportNode
from sigla.helpers.xml import load_xml_string_into_nodes


class TestXMLLoading:
    def test_one_element(self):
        node = ImportNode("a", {"name": "myname"}, [])
        source = dedent("""<a name="myname" />""")
        assert load_xml_string_into_nodes(source) == node

    def test_two_elements(self):
        nodes = ImportNode(
            "a", {"name": "a"}, [(ImportNode("b", {"name": "b"}, []))]
        )
        input = "<a name='a'><b name='b'></b></a>"
        assert load_xml_string_into_nodes(input) == nodes
