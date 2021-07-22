from abc import ABC, abstractmethod
from typing import List

from sigla.actions import Action, actions
from sigla.data.data import Data
from sigla.data.loaders import convert_xml_string_to_data
from sigla.template_loaders.template_loader import TemplateLoader


def join(lst_of_strings, separator="\n"):
    return separator.join(lst_of_strings)


def is_list(data: Data):
    return type(data) == list


def is_action(data: Data):
    return data.tag in actions.keys()


def map_and_join(map_function, the_list, *, sep=""):
    return join(
        map(
            map_function,
            the_list,
        ),
        sep,
    )


class RecursiveRender:
    def __init__(self, render_template, get_template, append_artifact):
        self.append_artifact = append_artifact
        self.render_template = render_template
        self.get_template = get_template

    def process_template(self, data):
        return self.render_template(data, template=self.get_template(data))

    def process_list(self, data, sep):
        return map_and_join(
            lambda c: self.render(c, sep=sep),
            data,
            sep=sep,
        )

    def render(self, data: Data = None, *, sep="\n"):

        if is_list(data):
            result = self.process_list(data, sep)

        elif is_action(data):
            result = self.process_list(data, sep)
            self.append_artifact(data, result)

        else:
            result = self.process_template(data)

        return result

    def __call__(self, *args, **kwargs):
        return self.render(*args, **kwargs)


class Engine(ABC):
    def __init__(self, data: Data, loader: TemplateLoader, *args, **kwargs):
        self.data = data
        self.loader = loader
        self.artifacts: List[Action] = []

    @classmethod
    def generate(cls, *args, **kwargs):
        engine = cls.render_from_xml(*args, **kwargs)
        for artifact in engine.artifacts:
            artifact.execute()
        return engine

    @classmethod
    def render_from_xml(cls, xml: str, *args, **kwargs):
        data = convert_xml_string_to_data(xml)
        return cls.render_from_data(data, *args, **kwargs)

    @classmethod
    def render_from_data(
        cls, data: Data, loader: TemplateLoader, *args, **kwargs
    ):
        engine = cls(data, loader, *args, **kwargs)
        engine.render(engine.data)
        return engine

    def render(self, _data: Data = None, *, sep="\n"):
        render = RecursiveRender(
            self.render_template, self.get_template, self.append_artifact
        )

        return render(
            _data,
            sep=sep,
        )

    def append_artifact(self, data, result):
        if action := actions.get(data.tag):
            self.artifacts.append(action(data, result))

    def get_template(self, data: Data):
        return self.loader.load(data.tag, bundle=data.get("bundle"))

    @abstractmethod
    def render_template(self, data: Data, template: str) -> str:
        pass
