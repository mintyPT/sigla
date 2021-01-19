from typing import Union, List

from jinja2 import Environment, BaseLoader, StrictUndefined

from sigla.lib2.FrontMatterHelper import FrontMatterHelper
from sigla.lib2.node.BaseNode import BaseNode


class NodeTemplate(BaseNode):

    def __init__(self, tag, attributes=None):
        super().__init__(tag, attributes)

    def process(self):
        str_tpl = self.template_loader(self.tag)

        self_front_matter = self.get_self_metadata()
        self.attributes.update(self_front_matter)

        for child in self.children:
            ctx = self.context.copy()
            ctx.update(self.attributes.copy())
            child.context = ctx
        return self.render_template(str_tpl)

    def render_template(self, str_tpl):
        def internal_render_method(something: Union[NodeTemplate, List[NodeTemplate]], sep=''):
            if isinstance(something, BaseNode):
                return something.process()
            else:
                return sep.join([node.process() for node in something])

        data = self.context.copy()
        data.update(self.attributes)
        return render(
            str_tpl,
            **data,
            meta=self.attributes,  # self
            children=self.children,
            render=internal_render_method,
        )

    def get_self_metadata(self):
        template = self.raw_template_loader(self.tag)
        fm_raw, template_content, handler = FrontMatterHelper.split(template)

        metadata = (
            FrontMatterHelper.parse(self.render_template(fm_raw), handler)
            if fm_raw and handler
            else {}
        )
        return metadata

    def template_loader(self, tag) -> str:
        template = self.raw_template_loader(tag)
        fm_raw, template_content, handler = FrontMatterHelper.split(template)
        return template_content

    def raw_template_loader(self, tag) -> str:
        raise NotImplementedError("Please implement raw_template_loader")


def render(tpl, **kwargs) -> str:
    env = Environment(loader=BaseLoader, undefined=StrictUndefined)
    template = env.from_string(tpl)
    return template.render(**kwargs)