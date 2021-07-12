from os import path
from typing import Any
from textwrap import dedent

from sigla import config
from sigla.data.data import Data, Attributes
from sigla.nodes.abstract_node import AbstractNode
from sigla.templates import TemplateEngineABC, TemplateLoaderABC
from sigla.nodes.node_list import NodeList
from sigla.utils.helpers import load_module, load_filters_from


class Node(AbstractNode):
    scripts_path = config.path.scripts

    def __init__(
            self,
            tag,
            engine: TemplateEngineABC,
            template_loader: TemplateLoaderABC,
            *,
            attributes=None,
            children=None,
            parent_attributes=None,
    ):

        if parent_attributes is None:
            parent_attributes = {}

        if children is None:
            children = NodeList()

        if attributes is None:
            attributes = {}

        self.context = {}

        self.data = Data(
            tag=tag,
            attributes=attributes,
            children=children,
            parent_attributes=parent_attributes,
        )

        self.loader = template_loader
        self.engine = engine

        self._handle_script_property()

    def _handle_script_property(self):
        """
            It's possible to pass a script prop to a tag and that script is
            expected to have a "main" function to be run.
            """
        if "script" not in self.data.attributes:
            return

        script = self.data.attributes["script"]

        module_path = path.join(self.scripts_path, script)

        new_attrs = _run_module_main_function(module_path, self)

        # handle returned value
        if new_attrs is None or type(new_attrs) != dict:
            raise ValueError(
                "Expected to receive a dictionary of new args"
            )

        self.data.attributes.update(**new_attrs)

    @property
    def attributes(self):
        return Attributes(
            self.data.frontmatter_attributes,
            self.data.attributes,
            self.data.parent_attributes,
        )

    @property
    def children(self):
        return NodeList(self.data.children)

    def flatten(self):
        return [self, *self.children.flatten()]

    def append(self, node: AbstractNode):
        self.data.children.append(node)
        return self

    def render(self, template, **kwargs):

        node = self
        filters = self.get_filters()

        try:
            return self.engine.render(
                template, filters=filters, **kwargs, node=node
            )
        except Exception as e:
            err_message = _generator_error_message(
                node=self, template=template
            )
            print(err_message)
            raise e

    def finish(self):
        return [child.finish() for child in self.children]

    def process(self):
        self._process()

    def _process(self):
        #
        self._render_string_attributes()
        #
        context = self._get_attributes_copy()
        for child in self.data.children:
            child.data.parent_attributes.update(**context)
        #
        for child in self.data.children:
            child.process()

    def _render_string_attributes(self):
        # update attributes
        attributes = self.data.attributes
        for key, value in attributes.items():
            if type(value) == str:
                attributes[key] = self.render(value, **self.attributes)

    def _get_attributes_copy(self):
        attributes = self.attributes
        context = self.context

        context = context.copy()
        context.update(dict(attributes))

        return context

    @staticmethod
    def get_filters():
        filters = load_filters_from(config.path.filters)
        return filters

    #
    def __getattr__(self, name: str) -> Any:
        if name in self.attributes:
            return self.attributes[name]
        raise AttributeError(f"{self.__class__.__name__}.{name} is invalid.")

    def __repr__(self) -> str:
        tag = self.data.tag
        attrs = self.attributes if len(self.attributes.keys()) > 0 else ""
        children = self.children if len(self.children) > 0 else ""
        return f"""<{tag} {attrs}>{children}</{self.data.tag}>"""

    def __eq__(self, other):
        return self.data == other.data


def _run_module_main_function(module_path, *args):
    # load module and execute it's `main` function
    module = load_module("s", module_path)
    new_attrs = module.main(*args)
    return new_attrs


def _generator_error_message(node=None, template=None):
    return dedent(
        f"""\
        ------------------------------
        ERROR WHILE RENDERING TEMPLATE
        ------------------------------

        TEMPLATE:
        {template}

        NODE:
        {node}

        ---

        """
    )
