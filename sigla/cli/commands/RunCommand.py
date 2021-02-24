from pathlib import Path
from typing import Union

import typer

from sigla import config, from_xml_string
from sigla.core.outputs.OutputEcho import OutputEcho
from sigla.core.outputs.OutputFile import OutputFile
from sigla.errors import TemplateDoesNotExistError
import abc


class AbstractDefinitionBasedCommand(abc.ABC, object):
    def __init__(self, references):
        self.references = references
        self.globs = [
            Path(config.path.definitions).glob(f"{reference}.xml")
            for reference in references
        ]
        self.matches = [match for glob in self.globs for match in glob]

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class RunCommand(AbstractDefinitionBasedCommand):
    @staticmethod
    def handle_results(s: Union[OutputFile, OutputEcho]):
        if isinstance(s, OutputFile):
            print(f":: Saving {s.path}")
            s.save()

    def handle_match(self, match):
        if not match.exists():
            raise typer.Exit(f"✋ The definition(s) do not exists {match}")

        is_dir = match.is_dir()

        if is_dir:
            return

        print(f":: Reading {match}")

        str_xml = match.read_text()
        results = from_xml_string(str_xml)()

        for output in results:
            self.handle_results(output)

    def __call__(self, *args, **kwargs):

        if len(self.matches) == 0:
            try:
                print(f"✋ No definition(s) found for {self.references}")
            except TemplateDoesNotExistError as e:
                print(e)
                raise typer.Exit(e)

        for match in self.matches:
            self.handle_match(match)
