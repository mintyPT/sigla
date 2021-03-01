from pathlib import Path
from typing import Union, Any

from sigla.utils import ensure_dirs


class OutputFile(object):
    def __init__(self, path, content):
        self.path = path
        self.content = content

    def save(self):
        ensure_dirs(Path(self.path).parent)
        with open(self.path, "w") as h:
            h.write(self.content)

    def __eq__(self, o: Union[Any, "OutputFile"]) -> bool:
        if type(self) == OutputFile and type(o) == OutputFile:
            if self.content == o.content and self.path == o.path:
                return True
        return False

    def __repr__(self):
        return f"[file-output: {self.content}]"
