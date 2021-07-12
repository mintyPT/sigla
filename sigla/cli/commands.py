from pathlib import Path

import typer

from sigla import __version__, config
from sigla.cli.actions import Action, NewDefinitionFile, NewFiltersFile
from sigla.main import process
from sigla.utils.errors import TemplateDoesNotExistError
from sigla.utils.helpers import ensure_dirs


class VersionCommand(Action):
    def run(self):
        self.log(f"Version: {__version__}")


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
        process("xml", str_xml, factory=None)

    def run(self):

        if len(self.matches) == 0:
            try:
                print(f"✋ No definition(s) found for {self.references}")
            except TemplateDoesNotExistError as e:
                print(e)
                raise typer.Exit(e)

        for match in self.matches:
            self.handle_definition_file_match(match)


class NewCommand(Action):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def run(self):
        cmd = NewDefinitionFile(config.path.definitions, self.name)
        cmd.run()


class InitCommand(Action):
    def run(self):
        self.log("sigla init")
        self.create_folder(
            config.path.templates,
            config.path.snapshots,
            config.path.definitions,
            config.path.scripts,
        )
        self.create_filters()

    def create_filters(self):
        self.log(f"- checking/creating file {config.path.filters}")
        cmd = NewFiltersFile(
            config.path.root_directory, config.path.filters_filename
        )
        cmd.run()

    def create_folder(self, *args):
        for path in args:
            self.log(f"- creating folder {path}")
            ensure_dirs(path)
