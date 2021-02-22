import textwrap

filter_file_default_content = textwrap.dedent(
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
