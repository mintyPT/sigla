from textwrap import dedent
from sigla.lib2.nodes.NodeTemplate import NodeTemplate


class MemoryNodeTemplate(NodeTemplate):
    def raw_template_loader(self, tag):
        if tag == "print-name":
            return "{{ name }}"
        if tag == "b":
            return "{{ name }}-{{ age }}"
        if tag == "person":
            return dedent(
                """
            ---
            second_name: "santos"
            ---
            {{- name }}-{{ second_name }}-{{ age }}
            """
            )
        if tag == "a":
            return "-a-{{ render(children) }}-a-"
        if tag == "a2":
            return "-a-{% for child in children %}{{ render(child) }}{% endfor %}-a-"
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
                """
            )
        if tag == "third-level":
            return dedent(
                """
                ---
                lower: "three"
                ---
                """
            )
        raise NotImplementedError(f"Missing memory template for {tag}")
