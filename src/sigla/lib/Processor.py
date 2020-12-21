import json

from sigla.lib.Node import Node
from sigla.lib.NodeTemplateLoader import NodeTemplateLoader
from sigla.lib.SiglaFile import SiglaFile
from sigla.lib.template.TemplateContext import TemplateContext
from sigla.lib.template.engines.njk import njk
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
            return list(map(self.process_node, node.children))

        if node.tag == "file":
            return self.process_file(node)

        else:
            return self.render_template(node)

    def process_nodes_to_str(self, node):
        nodes = map(self.process_node, cast_array(node))
        return "".join(nodes)

    def render_template(self, node):

        context = self.ctx.push_context(node)

        default_template = default_njk_template(json.dumps(list(context.keys()) + ["children"]))

        # load template
        loader = NodeTemplateLoader.from_node(node)
        loader.ensure(default_template)
        template, metadata = loader.load()

        result = njk(
            template,
            **context,
            children=node.children,
            render=self.process_nodes_to_str,
            context=(json.dumps(context)),
        )

        self.ctx.pop_context()
        return result
