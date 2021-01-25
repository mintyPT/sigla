from pathlib import Path

from sigla.lib.Config import Config


class CliConfig(Config):
    config: Path = Path.cwd().joinpath(".sigla/config.json")
    defaults = {
        "path_templates": ".sigla/templates",
        "path_snapshots": ".sigla/snapshots",
        "path_definitions": ".sigla/definitions",
        "path_filters": ".sigla/filters.py",
    }
