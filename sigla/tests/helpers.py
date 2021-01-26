from textwrap import dedent

from sigla.classes.errors import TemplateDoesNotExistError
from sigla.classes.nodes.NodeTemplate import NodeTemplate


class MemoryNodeTemplate(NodeTemplate):
    def raw_template_loader(self, tag):

        if tag == "apifier-root":
            return dedent(
                """
                ---
                name:  "sigla"
                ---
                def call_wrapper(url: str, method: str = "GET"):
                    def call(query, body, params):
                        print('call api')
                        print('- url:', url)
                        print('- method:', method)
                        print('- query:', query)
                        print('- body:', body)
                        print('- params:', params)
                    return call


                apifier = {
                {% for child in children %}
                    {{ render(child) | indent(8) }},
                {% endfor %}
                }"""
            )

        if tag == "apifier-block":
            return dedent(
                """
                ---
                name:  "sigla"
                ---
                "{{ name }}": { {% for child in children %}
                    {{ render(child) | indent(8) }},
                {%- endfor %}
                }"""
            )
        if tag == "apifier-call":
            return '"{{name}}": call_wrapper("/{{name}}", {{ attributes | without("name") | as_kwargs() }})'  # noqa

        if tag == "apifier-crud":
            return dedent(
                """
                "list": call_wrapper("{{ urlprefix }}/{{name}}", method="GET"),
                "create": call_wrapper("{{ urlprefix }}/{{name}}", method="POST"),
                "read": call_wrapper("{{ urlprefix }}/{{name}}/:id", method="GET"),
                "update": call_wrapper("{{ urlprefix }}/{{name}}/:id", method="PUT"),
                "update_p": call_wrapper("{{ urlprefix }}/{{name}}/:id", method="PUT"),
                "delete": call_wrapper("{{ urlprefix }}/{{name}}/:id", method="DELETE")
                """  # noqa
            )

        if tag == "print-name":
            return "{{ name }}"
        if tag == "b":
            return "{{ name }}-{{ age }}"
        if tag == "person":
            return dedent(
                """
            ---
            second_name: "sigla"
            ---
            {{- name }}-{{ second_name }}-{{ age }}
            """
            )
        if tag == "a":
            return "-a-{{ render(children) }}-a-"
        if tag == "a2":
            return "-a-{% for child in children %}{{ render(child) }}{% endfor %}-a-"  # noqa
        if tag == "ta":
            return "{{ render(children) }}"
        if tag == "tb":
            return "{{ render(children) }}"
        if tag == "tc":
            return "{{ ra }}{{ rb }}{{ name }}"

        if tag == "first-level":
            return dedent(
                """
                ---
                upper: "one"
                ---
                {{ render(children) }}
                """
            )
        if tag == "second-level":
            return dedent(
                """
                ---
                me: "two"
                ---
                {% set lower = bottom | flatten_deep | map_get("lower") | join(',') -%}
                __{{ upper }}/{{ me }}/{{ lower }}__
                """  # noqa
            )
        if tag == "third-level":
            return dedent(
                """
                ---
                lower: "three"
                ---
                """
            )
        raise TemplateDoesNotExistError(tag, self)
