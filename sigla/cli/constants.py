import json
import textwrap

filter_file_template = textwrap.dedent(
    """
    \"\"\"
    Export filters to use on the templates using the `FILTERS` variable
    \"\"\"
    import json


    def dump(var):
        return json.dumps(var, indent=4)


    FILTERS = {"dump": dump}
    """
)

new_definition_template = lambda name: textwrap.dedent(f"""\
    <root>
        <file name="output/{name}[.ext]">
            <{name}>
                [...]
            </{name}>
        </file>
    </root>
""")


def get_default_template_content(context):
    def default_jinja_template(dumped_context):
        return textwrap.dedent(f"""
            ---
            some_var: some_value
            ---

            Vars: {dumped_context}
            
            # render children 

            {{{{ render(children) }}}}

            # or

            {{% for child in children %}}
                {{{{ render(child) }}}}
            {{% endfor %}}

            """
        ).strip()

    json_context = json.dumps(list(context.keys()))
    return default_jinja_template(json_context)
