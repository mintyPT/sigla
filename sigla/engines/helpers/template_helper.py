from helpers.helpers import uniq, join
from sigla.engines.helpers.helpers import remove_none, get, dict_without_keys, as_kwargs
from sigla.engines.helpers.helpers_data import flatten


class TemplateHelper:
    def __init__(self, value):
        self.value = value

    def uniq(self):
        return TemplateHelper(uniq(self.value))

    def flatten(self):
        return TemplateHelper(flatten(self.value))

    def get(self, *args):
        return TemplateHelper(get(self.value, *args))

    def nonone(self):
        return TemplateHelper(remove_none(self.value))

    def join(self, sep):
        return TemplateHelper(join(self.value, separator=sep))

    def without(self, *args):
        return TemplateHelper(dict_without_keys(self.value, *args))

    def as_kwargs(self, sep=","):
        return TemplateHelper(as_kwargs(self.value, sep))

    def val(self):
        return self.value
