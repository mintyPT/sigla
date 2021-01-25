import logging
from pprint import pformat
from typing import Union, List
import pydash as _
from jinja2 import Environment, BaseLoader, StrictUndefined, UndefinedError, make_logging_undefined, Undefined

from sigla.lib2.helpers.FrontMatterHelper import FrontMatterHelper
from sigla.lib2.nodes.BaseNode import BaseNode


def render(tpl, filters=None, **kwargs) -> str:
    # logging.basicConfig()
    # logger = logging.getLogger('sigla')
    # LoggingUndefined = make_logging_undefined(logger=logger, base=Undefined)
    # env = Environment(loader=BaseLoader, undefined=LoggingUndefined)  # StrictUndefined
    env = Environment(loader=BaseLoader)

    env.filters["flatten"] = _.flatten
    env.filters["flatten_depth"] = _.flatten_depth
    env.filters["flatten_deep"] = _.flatten_deep
    env.filters["get"] = _.get
    env.filters["map"] = _.map_
    env.filters["filter"] = _.filter_
    env.filters["uniq"] = _.uniq
    env.filters["dump"] = pformat

    def as_kwargs_filter(obj):
        kwargs = []
        for k, v in obj.items():
            if type(v) == int:
                kwargs.append(f"{k}={v}")
            else:
                kwargs.append(f'{k}="{v}"')
        return ", ".join(kwargs)

    def map_get_filter(arr, key):
        return [_.get(o, key) for o in arr]

    def without_filter(obj, *args):
        result = {}
        for k, v in obj.items():
            if k not in args:
                result[k] = v
        return result

    def get_nested(arr, field):
        return map(lambda el: _.get(el, field), arr)

    env.filters["get_nested"] = get_nested
    env.filters["without"] = without_filter
    env.filters["as_kwargs"] = as_kwargs_filter
    env.filters["map_get"] = map_get_filter

    env.filters.update(filters)

    template = env.from_string(tpl)
    return template.render(**kwargs)


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
            return render(
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
            "bottom": (self.get_recursive_children_metadata()),  # data from children
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
        return template_content.strip()

    def raw_template_loader(self, tag) -> str:
        raise NotImplementedError("Please implement raw_template_loader")

    def get_filters(self):
        return {}
