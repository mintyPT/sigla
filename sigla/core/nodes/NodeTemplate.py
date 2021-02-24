import inspect
from pathlib import Path
from textwrap import dedent

from jinja2 import (
    UndefinedError,
)

from sigla.utils import (
    frontmatter_split,
    frontmatter_parse,
    import_node,
    import_node_list,
)
from sigla.core.renders.JinjaRenderer import JinjaRenderer

Node = import_node()
NodeList = import_node_list()


class NodeTemplate(Node):
    template_path = "./.sigla/templates/%s.jinja2"

    def process(self):
        super().process()
        return self.render_template(self.template_loader(self.data.tag))

    def render_template(self, str_tpl, **kwargs):
        try:
            renderer = JinjaRenderer()
            return renderer.render(
                str_tpl, filters=self.get_filters(), **kwargs, node=self
            )

        except UndefinedError as e:
            print(
                dedent(
                    f"""\
                    ------------------------------
                    ERROR WHILE RENDERING TEMPLATE
                    ------------------------------

                    TEMPLATE:
                    {str_tpl}

                    NODE:
                    {self}

                    ---

                    """
                )
            )

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
        fm_raw, template_content, handler = frontmatter_split(template)
        return template_content.strip()

    def raw_template_loader(self, tag) -> str:
        path = Path(self.template_path % tag)
        if path.exists() is False:
            variables = self.attributes

            methods_children = []
            for method in NodeList.methods:
                args = inspect.getfullargspec(getattr(NodeList, method)).args
                args = [a for a in args if a not in ["self"]]
                method = f".{method}" if method != "__call__" else ""
                methods_children.append(
                    f"node.children{method}({','.join(args)})"
                )

            content = self.render_template(
                dedent(
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
                ),
                variables=variables,
                methods=(list(methods_children)),
            )
            path.write_text(content)

        return path.read_text()

    @staticmethod
    def get_filters():
        return {}
