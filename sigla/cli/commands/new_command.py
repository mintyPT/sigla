from sigla import config
from sigla.cli.actions import NewDefinitionFile, Action


class NewCommand(Action):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def run(self):
        cmd = NewDefinitionFile(config.path.definitions, self.name)
        cmd.run()
