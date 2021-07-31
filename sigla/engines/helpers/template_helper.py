from typing import Any

from sigla.engines.helpers.flatten import Flatten
from sigla.engines.helpers.helpers import (
    as_kwargs,
    dict_without_keys,
    get,
    remove_none,
)
from sigla.helpers.helpers import join, uniq


class TemplateHelper:
    def __init__(self, value: Any) -> None:
        self.value = value

    def uniq(self) -> "TemplateHelper":
        return TemplateHelper(uniq(self.value))

    def flatten(self) -> "TemplateHelper":
        return TemplateHelper(Flatten()(self.value))

    def get(self, *args: Any) -> "TemplateHelper":
        return TemplateHelper(get(self.value, *args))

    def nonone(self) -> "TemplateHelper":
        return TemplateHelper(remove_none(self.value))

    def join(self, sep: str) -> "TemplateHelper":
        return TemplateHelper(join(self.value, separator=sep))

    def without(self, *args: str) -> "TemplateHelper":
        return TemplateHelper(dict_without_keys(self.value, *args))

    def as_kwargs(self, sep: str = ",") -> "TemplateHelper":
        return TemplateHelper(as_kwargs(self.value, sep))

    def val(self) -> Any:
        return self.value
