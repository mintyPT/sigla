from textwrap import dedent


def get_default_template():
    default_template_content = dedent(
        """\
        ---
        title: Lorem ipsum
        ---
        
        Here's what you can do inside this template (check the template, 
        not the result):
    
        Access the available properties on the current node. Them come from
        either the definition file or from the front matter section of the 
        template. As an example, we are showing you its current value.
            - {{ "{{ node.title}}" }}: Lorem ipsum
        {%- for key, value in node.attributes.items() %}
            - {{ "{{ node." + key + " }}" }}: {{value}}
        {%- else %}
            - none for now, so add some on the definition file or on the 
              front matter section
        {%- endfor %}
        
        --- 
                    
        If you wish to render its children, you can do that directly:
        {% raw %}
        {{ render(node.children) }}
        {% endraw %}
        
        Or iterating over node.children:
        {% raw %}
        {% for child in node.children %}
            {{ render(child) }}
        {% endfor %}
        {% endraw %}
    
        """  # noqa E501
    )
    return default_template_content
