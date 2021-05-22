from abc import ABC, abstractmethod
import typer
import textwrap
from pathlib import Path


class Action(ABC):
    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def log(msg):
        print(f"|> {msg}")


class NewFileAction(ABC):
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


class NewDefinitionFile(NewFileAction):
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


class NewFiltersFile(NewFileAction):
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
