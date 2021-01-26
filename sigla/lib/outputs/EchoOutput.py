from typing import Union


class EchoOutput:
    content: str = None

    def __init__(self, content):
        self.content = content

    def __eq__(self, o: Union[object, "EchoOutput"]) -> bool:
        if type(self) != type(o):
            return False
        if self.content != o.content:
            return False
        return True
