import json
import os
from pathlib import Path

from sigla.lib.helpers.files import ensure_parent_dir
from sigla.lib.helpers.loaders import load_template

from sigla.lib.Nodes.Node import Node
from sigla.lib.helpers.misc import cast_array

from sigla.lib.helpers.Context import Context
from sigla.lib.template.engines.njk import njk


def default_njk_template(dumped_context):
    return f"""

Available vars: {dumped_context}

Handle children:

{{{{ render(children) }}}}

{{% for child in children %}}
    {{{{ render(child) }}}}
{{% endfor %}}

"""


class NodeTemplateLoader:
    templates_directory = "./.sigla/templates"
    create_missing_templates = True

    def __init__(self, name):
        self.name = name
        self.path = Path(os.path.join(self.templates_directory, self.name))

    def ensure(self, default_value):
        """ Ensure the file really exists """

        if not self.create_missing_templates:
            return

        ensure_parent_dir(self.path)
        if self.path.exists():
            return
        with open(self.path, "w") as h:
            h.write(default_value)

    def load(self):
        return load_template(self.path)

    @classmethod
    def from_node(cls, node: Node):
        name = node.get_template_name()
        name = name.replace("-", "/")
        name = f"{name}.njk"

        return cls(name)


class TemplateNode(Node):

    def process_nodes_to_str(self, ctx=None):
        if ctx is None:
            ctx = Context()

        def wrapped(node):
            nodes = map(lambda e: e.process(ctx), cast_array(node))
            return "".join(nodes)

        return wrapped

    def process(self, ctx=None):
        if ctx is None:
            ctx = Context()

        context = ctx.push_context(self)

        default_template = default_njk_template(json.dumps(list(context.keys()) + ["children"]))

        # load template
        loader = NodeTemplateLoader.from_node(self)
        loader.ensure(default_template)
        template, metadata = loader.load()

        result = njk(
            template,
            **context,
            children=self.children,
            render=self.process_nodes_to_str(ctx),
            context=(json.dumps(context)),
        )

        ctx.pop_context()
        return result
