import json
from pathlib import Path

from sigla.lib.Node import Node
from sigla.lib.SiglaFile import SiglaFile
from sigla.lib.TemplateContext import TemplateContext
from sigla.lib.template_renderers.njk import render_njk
from sigla.lib.utils import cast_array, ensure_parent_dir

def default_njk_template(dumped_context):
    return f'''

Available vars: {dumped_context}


Handle children:

{{{{ render(children) }}}}

{{% for child in children %}}
    {{{{ render(child) }}}}
{{% endfor %}}


'''



class Processor:
    ctx = None
    templates_directory = './.sigla/templates'

    def __init__(self, ctx=None):
        if ctx is None:
            ctx = TemplateContext()
        self.ctx = ctx

    def process_file(self, node):

        if not node.name:
            raise Exception(f"# No name attached to the file element.")

        self.ctx.push_context(node)

        text = ''
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
            return self.render_template(node.otag, node)

    def process_nodes_to_str(self, node):
        nodes = map(self.process_node, cast_array(node))
        return ''.join(nodes)

    def render_template(self, name, node):
        create_missing_templates = True

        name = name.replace('-', '/')

        context = self.ctx.push_context(node)
        template_full_path = f"{self.templates_directory}/{name}.njk"
        dumped_context = json.dumps(context)
        dumped_context_keys = json.dumps(list(context.keys()) + ["children"])

        my_file = Path(template_full_path)
        if not my_file.exists() and create_missing_templates:
            ensure_parent_dir(template_full_path)
            with open(template_full_path, 'w') as h:
                h.write(default_njk_template(dumped_context_keys))

        result = render_njk(
            template_full_path,
            **context,
            children=node.children,
            render=self.process_nodes_to_str,
            context=dumped_context
        )

        self.ctx.pop_context()
        return result