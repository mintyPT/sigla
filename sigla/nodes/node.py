from os import path
from typing import Any
from textwrap import dedent

from sigla import config
from sigla.data.data import Data
from sigla.nodes.abstract_node import AbstractNode
from sigla.templates.engines import TemplateEngineABC
from sigla.nodes.node_list import NodeList
from sigla.utils.helpers import load_module, load_filters_from


class Node(AbstractNode):
    scripts_path = config.path.scripts

    def __init__(
        self,
        tag,
        engine: TemplateEngineABC,
        *,
        attributes=None,
        children=None,
        parent_attributes=None,
        context=None,
    ):

        self.children = children if children is not None else NodeList()
        self.context = context if context is not None else {}

        attributes = attributes if attributes is not None else {}

        parent_attributes = (
            parent_attributes if parent_attributes is not None else {}
        )

        self.data = Data(
            tag=tag,
            attributes=attributes,
            children=self.children,
            parent_attributes=parent_attributes,
        )

        self.engine = engine

        self._handle_script_property()

    def _handle_script_property(self):
        """
        It's possible to pass a script prop to a tag and that script is
        expected to have a "main" function to be run.
        """
        # TODO document this
        if "script" not in self.data.attributes:
            return

        script = self.data.attributes["script"]

        module_path = path.join(self.scripts_path, script)

        new_attrs = _load_and_run_module_main_function(module_path, self)

        # handle returned value
        if new_attrs is None or type(new_attrs) != dict:
            raise ValueError("Expected to receive a dictionary of new args")

        self.data.attributes.update(**new_attrs)

    @property
    def attributes(self):
        return self.data.get_attributes()

    def flatten(self):
        return [self, *self.children.flatten()]

    def append(self, node: AbstractNode):
        self.children.append(node)
        return self

    def render(self, template, **kwargs) -> str:

        node = self
        filters = self.get_filters()

        try:
            return self.engine.render(
                template, filters=filters, **kwargs, node=node
            )
        except Exception as e:
            err_message = _generate_error_message_for_rendering_exception(
                node=self, template=template
            )
            print(err_message)
            raise e

    def finish(self):
        return [child.finish() for child in self.children]

    def process(self):
        self._render_string_attributes()
        #
        context = self._get_attributes_copy()
        for child in self.children:
            child.update_parent_attributes(**context)
        #
        for child in self.children:
            child.process()

    def update_parent_attributes(self, **kwargs):
        self.data.parent_attributes.update(**kwargs)

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


def _load_and_run_module_main_function(module_path, *args, name="s"):
    # load module and execute it's `main` function
    module = load_module(name, module_path)
    return module.main(*args)


def _generate_error_message_for_rendering_exception(node=None, template=None):
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
