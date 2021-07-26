from pathlib import Path

from sigla.engines.engines import SiglaEngine


class DefinitionFile:
    def __init__(self, name):
        self.name = name
        self.filepath = Path(name)

    def exists(self):
        return self.filepath.exists()

    def write(self, content):
        self.filepath.write_text(content)

    def read(self):
        return self.filepath.read_text()

