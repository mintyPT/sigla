import frontmatter
import json
import os
from pathlib import Path
import pydash as _
from src.sigla.lib.Nodes.Node import Node
from src.sigla.lib.Nodes.template.engines.njk import njk
from src.sigla.lib.helpers.Context import Context
from src.sigla.lib.helpers.files import ensure_parent_dir


def load_template(filepath):
    with open(filepath, "r") as h:
        metadata, template = frontmatter.parse(h.read())
        return template, metadata


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


class NodeTemplate(Node):
    loader: NodeTemplateLoader
    template: str
    metadata = None
    kind = "template"

    def __init__(self, children=None, attributes=None, meta=None):
        super().__init__(children, attributes, meta)

        self.loader = NodeTemplateLoader.from_node(self)
        try:
            template, metadata = self.loader.load()
            self.template = template
            self.metadata = metadata
        except FileNotFoundError:
            pass

    def sub_process(self, ctx=None):
        if ctx is None:
            ctx = Context()

        def wrapped(node: Node):
            if type(node) == list:
                nodes = map(lambda e: e.process(ctx), node)
                return "".join(nodes)
            else:
                return node.process(ctx)

        return wrapped

    def process(self, ctx=None):
        if ctx is None:
            ctx = Context()

        context = ctx.push_context(self)

        template = self.template
        if not template:
            default_template = default_njk_template(
                json.dumps(list(context.keys()) + ["children"])
            )

            # load template
            self.loader.ensure(default_template)
            template, metadata = self.loader.load()

        flat_children = _.flatten(
            list(map(lambda x: x.flatten(), self.children))
        )

        all_meta = (
            _.chain(flat_children)
            .filter_(lambda x: type(x) == NodeTemplate)
            .map_("metadata")
            .filter_()
            .value()
        )

        result = njk(
            template,
            **context,
            children=self.children,
            meta=all_meta,
            render=self.sub_process(ctx),
            context=json.dumps(context),
        )

        ctx.pop_context()
        return result
