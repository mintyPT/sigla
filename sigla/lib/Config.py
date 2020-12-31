import json
import textwrap
from pathlib import Path


class Config(dict):
    """
    The helps keep local configuration for simple stuff like command line
    tools.

    To use, extend this class and add some defaults and the path to store the
    config.

    class SomeConfig(Config):
        config: Path = Path.cwd().joinpath('config.json')
        defaults = {
            "name": "James"
        }

    Then to use it

    > config = SiglaConfig()
    > config.load()
    > config['name'] = 'Bond'
    > config.save()

    """

    defaults = {}
    config: Path = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if self._config is None:
            warning_message = textwrap.dedent(
                """
                You need to override Config.config or Config.get_config
                with something like `Path.cwd().joinpath('config.json')`
            """
            )
            raise NotImplementedError(warning_message)

    def get_config(self) -> object:
        return None

    @property
    def _config(self):
        return self.config or self.get_config()

    def load(self):
        self.update(self.defaults)
        try:
            raw = self.config.read_text()
            if raw:
                self.update(json.loads(raw))
        except FileNotFoundError:
            pass

    def save(self):
        self.config.parent.mkdir(parents=True, exist_ok=True)
        self.config.write_text(json.dumps(self, indent=4))
