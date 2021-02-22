import json
import textwrap


def get_default_template_content(context):
    def default_jinja_template(dumped_context):
        return textwrap.dedent(
            f"""
            ---
            some_var: some_value
            ---

            Vars: {dumped_context}

            # render children

            {{{{ node.children() }}}}

            # or

            {{% for child in node.children %}}
                {{{{ child() }}}}
            {{% endfor %}}

            """
        ).strip()

    json_context = json.dumps(list(context.keys()))
    return default_jinja_template(json_context)
