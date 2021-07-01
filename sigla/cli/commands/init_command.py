from sigla import config
from sigla.cli.actions import NewFiltersFile, Action
from sigla.utils.helpers import ensure_dirs


class InitCommand(Action):
    def run(self):
        self.log("sigla init")
        self.create_folder(config.path.templates)
        self.create_folder(config.path.snapshots)
        self.create_folder(config.path.definitions)
        self.create_folder(config.path.scripts)
        self.create_filters()

    def create_filters(self):
        self.log(f"- checking/creating file {config.path.filters}")
        cmd = NewFiltersFile(
            config.path.root_directory, config.path.filters_filename
        )
        cmd.run()

    def create_folder(self, path):
        self.log(f"- creating folder {path}")
        ensure_dirs(path)
