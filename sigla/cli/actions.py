from abc import ABC, abstractmethod
import typer
import textwrap
from pathlib import Path

from sigla import config, load_node
from sigla.utils.errors import TemplateDoesNotExistError


class Action(ABC):
    @abstractmethod
    def run(self):
        pass


class FileAction(ABC):
    def __init__(self, path, name):
        self.path = path
        self.name = name

    @property
    @abstractmethod
    def content(self) -> str:
        pass

    @property
    def filepath(self):
        return Path(self.path).joinpath(f"{self.name}")

    def run(self):
        if self.filepath.exists():
            raise typer.Exit(f"✋ File {self.filepath} already exists")
        self.filepath.write_text(self.content)


class NewDefinitionFile(FileAction):
    extension = "xml"

    def __init__(self, path, name):
        super().__init__(path, name + ".xml")
        self.original_name = name

    @property
    def content(self):
        return textwrap.dedent(
            f"""\
            <root>
                <file to="output/{self.original_name}.txt">
                    <{self.original_name}>
                        [...]
                    </{self.original_name}>
                </file>
            </root>
        """
        )


class NewFiltersFile(FileAction):
    @property
    def content(self):
        return textwrap.dedent(
            """
            \"\"\"
            Export filters to use on the templates using the `FILTERS` variable
            \"\"\"
            import json
            from sigla import register_filter

            @register_filter('dump')
            def dump(var):
                return json.dumps(var, indent=4)

            """
        )


class RunCommand:
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

    def __call__(self, *args, **kwargs):

        if len(self.matches) == 0:
            try:
                print(f"✋ No definition(s) found for {self.references}")
            except TemplateDoesNotExistError as e:
                print(e)
                raise typer.Exit(e)

        for match in self.matches:
            self.handle_definition_file_match(match)
