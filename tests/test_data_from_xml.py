import unittest

from sigla.data.data import Data
from sigla.data.data_loaders.xml_to_data import convert_xml_string_to_data


class TestData(unittest.TestCase):
    def test_simple(self):
        provided = '<person name="mauro" age="34"></person>'
        expected = Data("person", name="mauro", age="34")

        result = convert_xml_string_to_data(provided)
        self.assertEqual(result, expected)

    def test_with_children(self):
        provided = """
            <persons>
                <person name="mauro" age="34"></person>
                <person name="santos" age="33"></person>
            </persons>
        """

        expected = Data(
            "persons",
            children=[
                Data("person", name="mauro", age="34"),
                Data("person", name="santos", age="33"),
            ],
        )

        result = convert_xml_string_to_data(provided)
        self.assertEqual(result, expected)

    def test_with_casting(self):
        provided = '<person name="mauro" age-int="34"></person>'
        expected = Data("person", name="mauro", age=34)

        result = convert_xml_string_to_data(provided)
        self.assertEqual(result, expected)

    def test_with_references(self):
        provided = """
            <root>
                <person name="mauro" age="34" id="mauro"></person>
                <pet name="ariel" age="3" owner-id="mauro" id="ariel" bundle="cenas"></pet>
            </root>
        """

        mauro2 = Data("person", name="mauro", age="34", bundle="cenas")

        expected = Data(
            "root",
            children=[
                (Data("person", name="mauro", age="34", id="mauro")),
                Data("pet", name="ariel", age="3", owner=mauro2, id="ariel", bundle="cenas"),
            ],
        )

        result = convert_xml_string_to_data(provided)

        self.assertEqual(result, expected)
