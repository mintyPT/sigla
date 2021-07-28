from abc import ABC, abstractmethod
from textwrap import dedent
from typing import List

import sigla.engines.helpers.helpers
from helpers.helpers import map_and_join
from sigla.actions.actions import Action, actions
from sigla.data.data import Data
from sigla.data.data_loaders.xml_to_data import convert_xml_string_to_data

from sigla.engines.helpers.helpers import get_default_template
from sigla.engines.helpers.helpers_data import get_template_path
from sigla.engines.helpers.template_helper import TemplateHelper
from sigla.external.frontmatter.frontmatter import (get_content,
                                                    parse_with_transformation)
from sigla.external.jinja2.jinja2 import render_template
from sigla.template_loaders.exceptions import TemplateDoesNotExistError
from sigla.template_loaders.template_loaders import TemplateLoader


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

        if hasattr(data, 'tag') and data.tag[0].isupper():
            # if the tag starts with an uppercase, we assume it's data and 
            # skip it
            # TODO add tests for this
            return ''

        elif type(data) == list:
            return self.process_list(data, sep)

        elif data.tag in actions.keys():
            result = self.process_list(data, sep)
            self.append_artifact(data, result)
            return result

        else:
            return self.process_template(data)

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
        return self.loader.load(get_template_path(data))

    @abstractmethod
    def render_template(self, data: Data, template: str) -> str:
        pass


def dump_data_and_template(data: Data, template: str):
    sep = "#" * 40
    small_sep = "#" * 10
    print(
        dedent(
            f"""
            {sep}
            {sep}

            {small_sep} === TEMPLATE === {small_sep}
            {template}

            {small_sep} === NODE === {small_sep}
            {data.render()}
            ---
            {data.attributes}

            {sep}
            {sep}

        """
        )
    )


class SiglaEngine(Engine):
    def __init__(
            self, data: Data, loader: TemplateLoader, *args, filters=None, **kwargs
    ):
        super().__init__(data, loader, *args, **kwargs)
        if filters is None:
            filters = {}
        self.filters = filters
        self.load_frontmatter(data=self.data)

    def render_template(self, data: Data, template: str) -> str:

        # TODO pass functions in?
        # TODO load functions from file?
        try:
            helper = TemplateHelper
            children = data.children
            render, filters = self.render, self.filters

            return render_template(
                template,
                _=helper,
                node=data,
                render=render,
                filters=filters,
                children=children,
                **data.attributes,
            )
        except Exception as e:
            dump_data_and_template(data, template)
            raise e

    def get_template(self, data: Data, raw=False):
        try:
            if raw:
                return super().get_template(data)
            else:
                # removes the frontmatter from the template
                template = super().get_template(data)
                return get_content(template).lstrip()
        except TemplateDoesNotExistError:
            return self.write_default_template(data)

    def write_default_template(self, data):
        content = self.get_new_template_for_data(data)
        self.write_template(data, content)
        return content

    def write_template(self, data: Data, content: str):
        self.loader.write(content, get_template_path(data))

    def load_frontmatter(self, *, data: Data = None) -> Data:
        tag_is_upper = data.tag[0].isupper()
        is_action = data.tag in actions.keys()

        if not is_action and tag_is_upper is False:
            data.own_attributes.update(**parse_with_transformation(
                self.get_template(data, raw=True),  # template
                self.render_template,
                data,
            ))

        if tag_is_upper is False:
            for child in data:
                self.load_frontmatter(data=child)

        return data

    def get_new_template_for_data(self, data: Data):
        return self.render_template(data, get_default_template())