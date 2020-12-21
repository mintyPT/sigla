import json
import os
from pathlib import Path

from sigla.lib.Node import Node
from sigla.lib.SiglaFile import SiglaFile
from sigla.lib.helpers.loaders import load_template
from sigla.lib.template.TemplateContext import TemplateContext
from sigla.lib.template.engines.njk import njk
from sigla.lib.helpers.files import ensure_parent_dir
from sigla.lib.helpers.misc import cast_array


def default_njk_template(dumped_context):
    return f"""

Available vars: {dumped_context}

Handle children:

{{{{ render(children) }}}}

{{% for child in children %}}
    {{{{ render(child) }}}}
{{% endfor %}}


"""


class TemplateLoader:
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


class Processor:
    ctx: TemplateContext = None

    def __init__(self, ctx=None):
        if ctx is None:
            ctx = TemplateContext()
        self.ctx = ctx

    def process_file(self, node: Node):

        if not node.name:
            raise Exception(f"# No name attached to the file element.")

        self.ctx.push_context(node)

        text = ""
        for child in node:
            text += self.process_node(child)

        self.ctx.pop_context()

        return SiglaFile(text, node.name)

    def process_node(self, node: Node):

        if node.tag == "root":
            process = self.process_node
            return list(map(process, node.children))

        if node.tag == "file":
            return self.process_file(node)

        else:
            # render a template
            return self.render_template(node)

    def process_nodes_to_str(self, node):
        nodes = map(self.process_node, cast_array(node))
        return "".join(nodes)

    def render_template(self, node):

        context = self.ctx.push_context(node)

        context_json = json.dumps(context)
        default_template_content = default_njk_template(json.dumps(list(context.keys()) + ["children"]))

        # load template
        loader = TemplateLoader.from_node(node)
        loader.ensure(default_template_content)
        template, metadata = loader.load()

        result = njk(
            template,
            **context,
            children=node.children,
            render=self.process_nodes_to_str,
            context=context_json,
        )

        self.ctx.pop_context()
        return result
