from sigla import __version__
from sigla.cli.actions import Action


class VersionCommand(Action):
    def run(self):
        self.log(f"Version: {__version__}")
