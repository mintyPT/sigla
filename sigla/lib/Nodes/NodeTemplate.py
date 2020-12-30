from pprint import pprint
from typing import Optional

import frontmatter
import json
import os
from pathlib import Path
import pydash as _
from frontmatter import u

from sigla.lib import Node
from sigla.lib.Nodes.Node import Node
from sigla.lib.Nodes.template.engines.njk import njk
from sigla.lib.helpers.Context import Context
from sigla.lib.helpers.files import ensure_parent_dir


#
# frontmatter utils
#
def fm_split(text, encoding="utf-8", handler=None):
    text = u(text, encoding).strip()

    # this will only run if a handler hasn't been set higher up
    handler = handler or frontmatter.detect_format(text, frontmatter.handlers)
    if handler is None:
        return None, text, None

    try:
        fm, content = handler.split(text)
    except ValueError:
        return None, text, handler

    return fm, content, handler


def fm_parse_fm(fm, handler, metadata=None):
    if metadata is None:
        metadata = {}

    fm = handler.load(fm)
    if isinstance(fm, dict):
        metadata.update(fm)

    return metadata


#
#
#


def get_default_template_content(context):
    def default_njk_template(dumped_context):
        return f"""
    
    Available vars: {dumped_context}
    
    Handle children:
    
    {{{{ render(children) }}}}
    
    {{% for child in children %}}
        {{{{ render(child) }}}}
    {{% endfor %}}
    
    """

    json_context = json.dumps(list(context.keys()) + ["children"])
    return default_njk_template(json_context)


class NodeTemplate(Node):
    template: Optional[str] = None
    kind = "template"
    templates_directory = "./.sigla/templates"
    create_missing_templates = True

    @property
    def template_name(self):
        name = self.get_template_name()
        name = name.replace("-", "/")
        name = f"{name}.njk"
        return name

    @property
    def template_path(self):
        return Path(os.path.join(self.templates_directory, self.template_name))

    #
    # metadata related stuff
    #
    def get_children_metadata(self, ctx):
        children = self.children

        if len(children) == 0:
            return None

        child: NodeTemplate
        metadata_ = []
        for child in children:
            if child.get_metadata:
                ctx.push_context(child)
                metadata_.append(child.get_metadata(ctx))
                ctx.pop_context()

        #
        metadata = _.filter_(metadata_, lambda x: x is not None)
        if len(metadata) > 0:
            return metadata

    def get_self_metadata(self, ctx):
        template = self.get_raw_template()
        if not template:
            return {}
        fm_raw, __, handler = fm_split(template)
        metadata = fm_parse_fm(self.render(fm_raw, ctx), handler) if fm_raw and handler else {}
        return metadata

    def get_metadata(self, ctx):
        metadata = self.get_self_metadata(ctx)
        children_metadata = self.get_children_metadata(ctx)

        if metadata is None and children_metadata is None:
            return None
        elif not children_metadata:
            return [metadata]
        else:
            return [metadata, children_metadata]

    def ensure_template(self, default_value):
        """ Ensure the file really exists """

        if self.get_raw_template() is not None:
            return

        if not self.create_missing_templates:
            return

        ensure_parent_dir(self.template_path)
        if self.template_path.exists():
            return
        with open(self.template_path, "w") as h:
            h.write(default_value)

    def get_raw_template(self):
        try:
            with open(self.template_path, 'r') as h:
                return h.read()
        except FileNotFoundError:
            pass

    def render(self, template, ctx, **kwargs):

        if ctx is None:
            ctx = Context()

        context = ctx.get_context()

        result = njk(
            template,
            **context,
            ctx=context,
            children=self.children,
            **kwargs,
        )

        return result

    def process(self, ctx=None):

        if ctx is None:
            ctx = Context()
        ctx.push_context(self)

        self.ensure_template(get_default_template_content(ctx.get_context()))

        fm_raw, body_raw, handler = fm_split(self.get_raw_template())

        metadata = self.get_children_metadata(ctx)
        self_metadata = self.get_self_metadata(ctx)

        def f(e):
            return e.process(ctx)

        def wrapped(node: Node, sep="\n"):
            if type(node) == list:
                nodes = map(f, node)
                return sep.join(nodes)
            return f(node)

        #
        res = self.render(
            body_raw,
            ctx,
            meta=metadata,
            render=wrapped,
            **self_metadata
        )
        ctx.pop_context()

        return res
