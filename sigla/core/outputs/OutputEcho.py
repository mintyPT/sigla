from typing import Union, Any


class OutputEcho(object):
    def __init__(self, content):
        self.content = content

    def __eq__(self, o: Union[Any, "OutputEcho"]) -> bool:
        if type(self) == OutputEcho and type(o) == OutputEcho:
            if self.content == o.content:
                return True
        return False

    def __repr__(self):
        return f"[echo-output: {self.content}]"
