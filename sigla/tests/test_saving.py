from sigla.helpers.importers import from_import_node_to_base_node
from sigla.helpers.xml import load_xml_string_into_nodes
from sigla.lib.outputs.EchoOutput import EchoOutput
from sigla.lib.outputs.FileOutput import FileOutput
from sigla.tests.helpers import MemoryNodeTemplate


class TestSaving:
    def test_fm_child(self):
        provided = """
            <root>
                <file to="result.txt">
                    <print-name name="sigla"/>
                </file>
                <echo>
                    <print-name name="sigla"/>
                </echo>
            </root>
        """
        got = from_import_node_to_base_node(
            load_xml_string_into_nodes(provided), TemplateClass=MemoryNodeTemplate
        ).process()
        expected = [
            FileOutput(path="result.txt", content="sigla"),
            EchoOutput(content="sigla"),
        ]

        assert got == expected
