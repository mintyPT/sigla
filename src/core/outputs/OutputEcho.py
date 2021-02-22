from typing import Union


class OutputEcho:
    content: str = None

    def __init__(self, content):
        self.content = content

    def __eq__(self, o: Union[object, "OutputEcho"]) -> bool:
        if type(self) != type(o):
            return False
        if self.content != o.content:
            return False
        return True

    def __repr__(self):
        return f"[echo-output: {self.content}]"
