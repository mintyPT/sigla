from textwrap import dedent

from jinja2 import UndefinedError

from sigla import config
from sigla.FrontMatter import FrontMatter
from sigla.nodes.Node import Node
from sigla.nodes.NodeList import NodeList
from sigla.templates.engines import JinjaEngine
from sigla.templates.loaders import FileTemplateLoader
from sigla.utils.helpers import load_filters_from


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
            engine = JinjaEngine()
            return engine.render(
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

        fm = FrontMatter()
        fm_raw, template_content, handler = fm.split(template)

        if fm_raw and handler:
            frontmatter = self.render_template(fm_raw)
            fm1 = FrontMatter(handler)
            metadata = fm1.parse(frontmatter, metadata=None)
        else:
            metadata = {}

        return metadata

    def template_loader(self, tag) -> str:
        template = self.raw_template_loader(tag)

        fm = FrontMatter()
        frontmatter, content, handler = fm.split(template)

        return content.strip()

    def raw_template_loader(self, tag) -> str:
        path = self.get_template_path(tag)

        if path.exists() is False:
            self.create_default_template(path)

        return path.read_text()

    def create_default_template(self, path):
        variables = self.attributes
        methods = NodeList.get_node_list_methods()
        content = self.render_template(
            default_template_content,
            variables=variables,
            methods=list(methods),
        )
        path.write_text(content)

    def get_template_path(self, tag):
        bundle = self.attributes.get("bundle")
        loader = FileTemplateLoader(self.base_path, "jinja2")
        path = loader.load(tag, bundle)
        return path

    @staticmethod
    def get_filters():
        return load_filters_from(config.path.filters)
