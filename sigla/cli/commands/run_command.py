from pathlib import Path

import typer

from sigla import config, load_node
from sigla.cli.actions import Action
from sigla.utils.errors import TemplateDoesNotExistError


class RunCommand(Action):
    def __init__(self, references):
        self.references = references
        self.globs = [
            Path(config.path.definitions).glob(f"{reference}.xml")
            for reference in references
        ]
        self.matches = [match for glob in self.globs for match in glob]

    @staticmethod
    def handle_definition_file_match(match):
        if not match.exists():
            raise typer.Exit(f"✋ The definition(s) do not exists {match}")

        is_dir = match.is_dir()

        if is_dir:
            return

        print(f":: Reading {match}")

        str_xml = match.read_text()
        nodes = load_node("xml_string", str_xml, factory=None)
        nodes.process()
        nodes.finish()

    def run(self):

        if len(self.matches) == 0:
            try:
                print(f"✋ No definition(s) found for {self.references}")
            except TemplateDoesNotExistError as e:
                print(e)
                raise typer.Exit(e)

        for match in self.matches:
            self.handle_definition_file_match(match)
