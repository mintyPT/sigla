from collections import ChainMap
from copy import deepcopy


class Attributes(ChainMap):
    def without(self, name):
        data = deepcopy(dict(self))
        del data[name]
        return Attributes(data)

    def as_kwargs(self, sep=","):
        kwargs = []
        for k, v in self.items():
            if type(v) == int:
                kwargs.append(f"{k}={v}")
            else:
                kwargs.append(f'{k}="{v}"')
        if sep:
            return ", ".join(kwargs)
        return kwargs
