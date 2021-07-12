from textwrap import dedent
from sigla.front_matter import FrontMatter
from sigla.nodes.node import Node
from sigla.nodes.node_list import NodeList
from sigla.templates import TemplateEngineABC, TemplateLoaderABC
from sigla.utils.errors import TemplateDoesNotExistError


class NodeTemplate(Node):
    create_template = True

    def finish(self):
        raise NotImplementedError

    def process(self):
        self._process()
        return self._potato()

    def _process(self):
        self.data.frontmatter_attributes = self._get_metadata()
        super()._process()

    def _potato(self):
        # load template for tag
        raw_template = self.load_template(self.data.tag)
        # handle frontmatter
        return self.render(_get_template_without_frontmatter(raw_template))

    def _get_metadata(self):
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
        create_template = self.create_template
        default_template = self.create_default_template()

        if path.exists() is False:
            if create_template:
                path.write_text(default_template)
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


def _get_template_without_frontmatter(template):
    fm = FrontMatter()
    frontmatter, content, handler = fm.split(template)
    tpl = content.strip()
    return tpl
