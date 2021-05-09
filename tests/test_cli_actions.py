import unittest
from os.path import join
from tempfile import TemporaryDirectory
from sigla.cli.actions import NewDefinitionFile, NewFiltersFile


class TestNewDefinitionFile(unittest.TestCase):
    def test_one(self):
        with TemporaryDirectory() as p:
            cmd = NewDefinitionFile(p, "random")
            cmd.run()

            with open(join(p, "random.xml")) as h:
                content = h.read()
                self.assertIn("<root>", content)


class TestNewFiltersFile(unittest.TestCase):
    def test_one(self):
        with TemporaryDirectory() as p:
            cmd = NewFiltersFile(p, "random.py")
            cmd.run()

            with open(join(p, "random.py")) as h:
                content = h.read()
                self.assertIn("Export filters to use on the te", content)
