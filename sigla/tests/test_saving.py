from sigla.lib2.funcs import from_import_node_to_base_node
from sigla.lib2.importers.xml import load_xml
from sigla.lib2.outputs.EchoOutput import EchoOutput
from sigla.lib2.outputs.FileOutput import FileOutput
from sigla.tests.helpers import MemoryNodeTemplate


class TestSaving:
    def test_fm_child(self):
        provided = """
            <root>
                <file to="result.txt">
                    <print-name name="mauro"/>
                </file>
                <echo>
                    <print-name name="mauro"/>
                </echo>
            </root>
        """
        got = from_import_node_to_base_node(
            load_xml(provided), TemplateClass=MemoryNodeTemplate
        ).process()
        expected = [
            FileOutput(path="result.txt", content="mauro"),
            EchoOutput(content="mauro"),
        ]

        assert got == expected
