from pprint import pformat
from typing import Union, List
from jinja2 import (
    UndefinedError,
)

from sigla.classes.FrontMatter import FrontMatter
from sigla.classes.nodes.BaseNode import BaseNode
from sigla.helpers.renderers import jinja_render


class NodeTemplate(BaseNode):
    def __init__(self, tag, attributes=None):
        super().__init__(tag, attributes)

    def __repr__(self):
        return f"<{self.tag} {self.attributes}>"

    def process(self):
        super().process()
        return self.render_template(self.template_loader(self.tag))

    def render_template(self, str_tpl):
        def internal_render_method(
                something: Union[NodeTemplate, List[NodeTemplate]], sep="\n"
        ):
            if isinstance(something, BaseNode):
                return something.process()
            else:
                return sep.join([node.process() for node in something])

        kwargs = self.get_data_for_template()

        try:
            return jinja_render(
                str_tpl,
                **kwargs,
                filters=self.get_filters(),
                render=internal_render_method,
            )
        except UndefinedError as e:
            print("=== TEMPLATE ===")
            print(str_tpl)
            print("---")
            print(pformat(kwargs))
            print("=== TEMPLATE ===")
            raise e

    def get_data_for_template(self):
        kwargs = {
            **self.context.copy(),
            **self.attributes,
            "attributes": self.attributes,  # data from self
            "context": self.context,  # data from parents
            "bottom": (
                self.get_recursive_children_metadata()
            ),  # data from children
            "children": self.children,
        }
        return kwargs

    def update_context(self):
        self.attributes.update(self.get_self_metadata())
        super().update_context()

    def get_recursive_children_metadata(self):
        data = []
        for child in self.children:
            data.append(
                [child.attributes, child.get_recursive_children_metadata()]
            )
        return data

    def get_self_metadata(self):
        template = self.raw_template_loader(self.tag)
        fm_raw, template_content, handler = FrontMatter.split(template)

        metadata = (
            FrontMatter.parse(self.render_template(fm_raw), handler)
            if fm_raw and handler
            else {}
        )
        return metadata

    def template_loader(self, tag) -> str:
        template = self.raw_template_loader(tag)
        fm_raw, template_content, handler = FrontMatter.split(template)
        return template_content.strip()

    def raw_template_loader(self, tag) -> str:
        raise NotImplementedError("Please implement raw_template_loader")

    def get_filters(self):
        return {}
