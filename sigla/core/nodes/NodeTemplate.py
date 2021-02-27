import inspect
from pathlib import Path
from textwrap import dedent

from jinja2 import (
    UndefinedError,
)

from sigla import config
from sigla.core.renders import render
from sigla.utils import (
    frontmatter_split,
    frontmatter_parse,
    import_node,
    import_node_list,
)

Node = import_node()
NodeList = import_node_list()


def get_template_path(base_path, tag, ext="jinja2", bundle=None):
    path = Path(base_path)
    if bundle:
        path = path.joinpath(bundle)
    path = path.joinpath(f"{tag}.{ext}")
    return path


def get_default_error_message(node, str_tpl):
    return dedent(
        f"""\
        ------------------------------
        ERROR WHILE RENDERING TEMPLATE
        ------------------------------

        TEMPLATE:
        {str_tpl}

        NODE:
        {node}

        ---

        """
    )


default_template_content = dedent(
    """\
    ---
    title: Generating code like it's 99
    ---

    You can use variables written inside the frontmatter:
        - {% raw %}{{ node.title }}{% endraw %}: Generating code like it's 99

    Available variables (with current values for first node as an example):
    {%- for key, value in variables.items() %}
        - {{ "{{ node." + key + " }}" }}: {{value}}
    {%- else %}
        - none for now
    {%- endfor %}

    Methods available on node.children:
    {%- for value in methods %}
        - {{ value }}
    {%- endfor %}

    You can also iterate over node.children and access variables, render, ...
    {% raw %}
    {% for child in node.children %}
        {{ child() }}
    {% endfor %}
    {% endraw %}

    """  # noqa E501
)


class NodeTemplate(Node):
    base_path = config.path.templates

    def process(self):
        super().process()
        return self.render_template(self.template_loader(self.data.tag))

    def render_template(self, str_tpl, **kwargs):
        try:
            return render(
                "jinja",
                str_tpl,
                filters=self.get_filters(),
                **kwargs,
                node=self,
            )

        except UndefinedError as e:
            err_message = get_default_error_message(self, str_tpl)
            print(err_message)
            raise e

    def update_context(self):
        metadata = self.get_self_metadata()
        self.data.frontmatter_attributes = metadata
        super().update_context()

    def get_self_metadata(self):
        template = self.raw_template_loader(self.data.tag)
        fm_raw, template_content, handler = frontmatter_split(template)

        metadata = (
            frontmatter_parse(self.render_template(fm_raw), handler)
            if fm_raw and handler
            else {}
        )
        return metadata

    def template_loader(self, tag) -> str:
        template = self.raw_template_loader(tag)
        frontmatter, content, handler = frontmatter_split(template)
        return content.strip()

    def raw_template_loader(self, tag) -> str:
        path = self.get_template_path(tag)

        if path.exists() is False:
            variables = self.attributes

            methods_children = NodeList.get_node_list_methods()

            content = self.render_template(
                default_template_content,
                variables=variables,
                methods=(list(methods_children)),
            )
            
            path.write_text(content)

        return path.read_text()

    def get_template_path(self, tag):
        path = get_template_path(
            self.base_path,
            tag,
            "jinja2",
            bundle=(self.attributes.get("bundle")),
        )
        return path

    @staticmethod
    def get_filters():
        return {}
