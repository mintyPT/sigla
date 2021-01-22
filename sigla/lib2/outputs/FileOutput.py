from typing import Union


class FileOutput:
    path: str = None
    content: str = None

    def __init__(self, path, content):
        self.path = path
        self.content = content

    def __eq__(self, o: Union[object, "FileOutput"]) -> bool:
        if type(self) != type(o):
            return False
        if self.content != o.content:
            return False
        if self.path != o.path:
            return False
        return True
