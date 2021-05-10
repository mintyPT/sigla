from os import path
from textwrap import dedent
from typing import Any

from jinja2 import UndefinedError

from sigla import config
from sigla.data.Data import Data
from sigla.nodes.NodeABC import NodeABC
from sigla.nodes.NodeList import NodeList
from sigla.templates.engines import JinjaEngine
from sigla.templates.loaders import FileTemplateLoader
from sigla.utils.helpers import load_module, load_filters_from


class Node(NodeABC):
    base_path = config.path.templates
    scripts_base_path = config.path.scripts

    def __init__(
        self, tag, attributes=None, children=None, parent_attributes=None
    ):
        if parent_attributes is None:
            parent_attributes = {}
        if children is None:
            children = []
        if attributes is None:
            attributes = {}

        self.context = {}
        self.data = Data(
            tag=tag,
            attributes=attributes,
            children=children,
            parent_attributes=parent_attributes,
        )

        self.loader = FileTemplateLoader(self.base_path, "jinja2")
        self.engine = JinjaEngine()

        self.handle_script_prop(attributes)

    def handle_script_prop(self, attributes):
        if "script" in self.data.attributes:
            module = load_module(
                "s", path.join(self.scripts_base_path, attributes["script"])
            )
            new_attrs = module.main(self)
            if new_attrs is not None and type(new_attrs) == dict:
                self.data.attributes.update(**new_attrs)

    def update_attributes(self):
        for key, value in self.data.attributes.items():
            if type(value) == str:
                new_value = self.render(value, **self.attributes)
                if new_value != value:
                    self.data.attributes[key] = new_value

    @property
    def attributes(self):
        return self.data.all_attributes

    @property
    def children(self):
        return NodeList(self.data.children)

    def flatten(self):
        return [self, *self.children.flatten()]

    def append(self, node: NodeABC):
        self.data.children.append(node)
        return self

    def render(self, str_tpl, **kwargs):

        try:
            return self.engine.render(
                str_tpl,
                filters=self.get_filters(),
                **kwargs,
                node=self,
            )

        except UndefinedError as e:
            err_message = self.error_message(self, str_tpl)
            print(err_message)
            raise e

    def process(self):
        self.update_context()

    def update_parent_context(self, ctx):
        self.data.parent_attributes.update(**ctx)

    def update_context(self):
        for child in self.data.children:
            ctx = self.context.copy()
            ctx.update(dict(self.attributes))
            child.update_parent_context(ctx)
            child.update_context()
        self.update_attributes()

    #
    def __getattr__(self, name: str) -> Any:
        if name in self.attributes:
            return self.attributes[name]
        raise AttributeError(f"{self.__class__.__name__}.{name} is invalid.")

    def __repr__(self) -> str:
        tag = self.data.tag
        attrs = self.attributes if len(self.attributes.keys()) > 0 else ""
        children = self.children if len(self.children) > 0 else ""
        return dedent(f"""<{tag} {attrs}>{children}</{self.data.tag}>""")

    def __eq__(self, other):
        return self.data == other.data

    @staticmethod
    def get_filters():
        filters = load_filters_from(config.path.filters)
        return filters
