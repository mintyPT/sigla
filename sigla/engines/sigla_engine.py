from textwrap import dedent

from sigla.actions import actions
from sigla.data.data import Data
from sigla.data.errors import DataKeyError
from sigla.deps.frontmatter.frontmatter import (get_content,
                                                parse_with_transformation)
from sigla.deps.jinja2.jinja2 import render_template
from sigla.engines.engine import Engine
from sigla.engines.helpers.default_template import get_default_template
from sigla.engines.helpers.template_helper import TemplateHelper
from sigla.template_loaders.errors import TemplateDoesNotExistError
from sigla.template_loaders.template_loader import TemplateLoader


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
        except DataKeyError as e:
            dump_data_and_template(data, template)
            raise e

    def get_template(self, data: Data, raw=False):
        try:
            template = super().get_template(data)
            if not raw:
                # removes the frontmatter from the template
                template = get_content(template).lstrip()
            return template
        except TemplateDoesNotExistError:
            content = self.get_new_template_for_data(data)
            self.write_template(data, content)
            return content

    def write_template(self, data: Data, content: str):
        self.loader.write(content, data.tag, bundle=data.get("bundle"))

    def load_frontmatter(self, *, data: Data = None) -> Data:
        if data.tag not in actions.keys():
            frontmatter = parse_with_transformation(
                self.get_template(data, raw=True),  # template
                self.render_template,
                data,
            )
            data.own_attributes.update(**frontmatter)

        for child in data:
            self.load_frontmatter(data=child)

        return data

    def get_new_template_for_data(self, data: Data):
        return self.render_template(data, get_default_template())
