from copy import deepcopy


class TemplateHelper:
    def __init__(self, value):
        self.value = value

    def flatten(self):
        def flatten(items):
            ret = []
            for item in items:
                ret.append(item)
                for child in item:
                    ret += flatten(child)
            return ret

        self.value = flatten(self.value)
        return self

    def get(self, key):
        self.value = [getattr(item, key) for item in self.value if item]
        return self

    def nonone(self):
        self.value = [item for item in self.value if item]
        return self

    def join(self, sep):
        self.value = sep.join(self.value)
        return self

    def val(self):
        return self.value

    def without(self, *args):
        data = deepcopy(dict(self.value))
        for name in args:
            del data[name]
        self.value = data
        return self

    def as_kwargs(self, sep=","):
        kwargs = []
        # TODO replace with json.dumps
        for k, v in self.value.items():
            if type(v) == int:
                kwargs.append(f"{k}={v}")
            else:
                kwargs.append(f'{k}="{v}"')
        if sep:
            self.value = ", ".join(kwargs)
            return self
        self.value = kwargs
        return self
