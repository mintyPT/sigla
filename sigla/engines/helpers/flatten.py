from typing import Any, List

from sigla.data.data import Data


class Flatten:
    def __init__(self):
        self.ret = []

    def _add(self, *elements):
        for element in elements:
            self.ret.append(element)

    def __call__(self, lst: Any) -> List:
        """
        Recursively flattens a list
        """
        for item in lst:
            self.handle_element(item)
            self.handle_children(item)

        return self.ret

    def handle_children(self, item: Any) -> None:
        for child in item:
            flt = Flatten()
            self._add(*flt(child) if type(child) == list else child)

    def handle_element(self, item: Any) -> None:
        if type(item) == Data:
            self._add(item)
