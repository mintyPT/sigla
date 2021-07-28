from copy import deepcopy
from textwrap import dedent

from helpers.helpers import join


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


def remove_none(value):
    return [item for item in value if item]


def get(obj, key):
    if type(obj) == list:
        return [item.get(key) for item in obj if item]
    else:
        return obj.get(key)


def dict_without_keys(value, *args):
    data = deepcopy(dict(value))
    for name in args:
        if name in data.keys():
            del data[name]
    return data


def as_kwargs(obj, sep):
    # TODO replace with json.dumps

    kwargs = []

    for k, v in obj.items():
        if type(v) in [int, bool]:
            kwargs.append(f"{k}={v}")
        else:
            kwargs.append(f'{k}="{v}"')

    if sep:
        return join(kwargs, sep)
    else:
        return kwargs