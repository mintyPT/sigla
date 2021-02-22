from pathlib import Path
from pprint import pformat
from jinja2 import (
    UndefinedError,
)
from core.nodes.Node import Node
from core.renders.JinjaRenderer import JinjaRenderer
from core import split, parse


class NodeTemplate(Node):
    template_path = "./.sigla/templates/%s.jinja2"

    def process(self):
        super().process()
        return self.render_template(self.template_loader(self.data.tag))

    def render_template(self, str_tpl):
        try:

            renderer = JinjaRenderer()
            return renderer.render(
                str_tpl, filters=self.get_filters(), node=self
            )

        except UndefinedError as e:
            print("=== TEMPLATE ===")
            print(str_tpl)
            print("---")
            print(
                pformat(
                    {
                        "node": self,
                    }
                )
            )
            print("=== TEMPLATE ===")
            raise e

    def update_context(self):
        metadata = self.get_self_metadata()
        self.data.frontmatter_attributes = metadata
        super().update_context()

    def get_self_metadata(self):
        template = self.raw_template_loader(self.data.tag)
        fm_raw, template_content, handler = split(template)

        metadata = (
            parse(self.render_template(fm_raw), handler)
            if fm_raw and handler
            else {}
        )
        return metadata

    def template_loader(self, tag) -> str:
        template = self.raw_template_loader(tag)
        fm_raw, template_content, handler = split(template)
        return template_content.strip()

    def raw_template_loader(self, tag) -> str:
        return Path(self.template_path % tag).read_text()
        # raise NotImplementedError
        # (f"Please implement raw_template_loader: {self.__class__.__name__}")

    def get_filters(self):
        return {}
