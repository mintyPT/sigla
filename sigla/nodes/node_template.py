from textwrap import dedent
from sigla.frontmatter.frontmatter import FrontMatter
from sigla.nodes.node import Node
from sigla.nodes.node_list import NodeList
from sigla.templates.engines import TemplateEngineABC
from sigla.templates.loaders import TemplateLoaderABC
from sigla.utils.errors import TemplateDoesNotExistError


class NodeTemplate(Node):
    create_template = True

    def __init__(
        self,
        tag,
        engine: TemplateEngineABC,
        template_loader: TemplateLoaderABC,
        **kwargs
    ):
        super().__init__(tag, engine, **kwargs)

        self.loader = template_loader

    def finish(self):
        msg = (
            "This is a template node. It should probably not be the first "
            "one to be called"
        )
        raise NotImplementedError(msg)

    def process(self):
        self.data.frontmatter = self._get_frontmatter_from_template()
        super().process()

        # load template for tag
        template = self._get_template_without_frontmatter()

        # handle frontmatter
        return self.render(template)

    #
    #
    #

    def _get_frontmatter_from_template(self):
        raw_template = self._get_raw_template()

        frontmatter = FrontMatter()
        frontmatter_str, template, handler = frontmatter.split(raw_template)

        if not frontmatter or not handler:
            return {}

        content = self.render(frontmatter_str)
        return FrontMatter.parse_with_handler(handler, content)

    def _get_raw_template(self):
        bundle = self.attributes.get("bundle")
        exists = self.loader.exists(self.data.tag, bundle=bundle)
        if not exists:
            if self.create_template:
                default_template = self._create_default_template()
                path = self.loader.get_path(self.data.tag, bundle=bundle)
                path.write_text(default_template)
            else:
                raise TemplateDoesNotExistError(self.data.tag, self)
        return self.loader.read(self.data.tag, bundle=bundle)

    def _get_template_without_frontmatter(self):
        raw_template = self._get_raw_template()
        template = FrontMatter().get_content(raw_template)
        return template

    def _create_default_template(self):

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
        # TODO look into this and document it
        methods = NodeList.get_node_list_methods()

        content = self.render(
            default_template_content,
            variables=variables,
            methods=list(methods),
        )
        return content
