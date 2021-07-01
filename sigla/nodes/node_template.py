from textwrap import dedent
from sigla.front_matter import FrontMatter
from sigla.nodes.node import Node
from sigla.nodes import PublicNodeABC
from sigla.nodes.node_list import NodeList
from sigla.utils.errors import TemplateDoesNotExistError


class NodeTemplate(PublicNodeABC, Node):
    create_template = True

    def process(self):
        super().process()

        # load template for tag
        template = self.load_template(self.data.tag)

        # handle frontmatter
        fm = FrontMatter()
        frontmatter, content, handler = fm.split(template)
        tpl = content.strip()

        return self.render(tpl)

    def finish(self):
        raise NotImplementedError

    def update_context(self):
        metadata = self.get_metadata()
        self.data.frontmatter_attributes = metadata
        super().update_context()

    def get_metadata(self):
        template = self.load_template(self.data.tag)

        fm = FrontMatter()
        fm_raw, template_content, handler = fm.split(template)

        if fm_raw and handler:
            frontmatter = self.render(fm_raw)
            fm1 = FrontMatter(handler)
            metadata = fm1.parse(frontmatter, metadata=None)
        else:
            metadata = {}

        return metadata

    def get_template_path(self, tag):
        return self.loader.load(tag, bundle=(self.attributes.get("bundle")))

    def load_template(self, tag) -> str:
        path = self.get_template_path(tag)

        if path.exists() is False:
            if self.create_template:
                content = self.create_default_template()
                path.write_text(content)
            else:
                raise TemplateDoesNotExistError(tag, self)

        return path.read_text()

    def create_default_template(self):

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

        variables = self.attributes
        methods = NodeList.get_node_list_methods()
        content = self.render(
            default_template_content,
            variables=variables,
            methods=list(methods),
        )
        return content
