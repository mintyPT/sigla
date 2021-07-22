import importlib
import textwrap
import types
from contextlib import suppress

import typer


def log(msg, kind="default"):
    """
    Log message
    """
    # TODO make this delightful
    if kind == "default":
        typer.secho(f" 🚀 sigla :: {msg}", fg="green")
    elif kind == "error":
        typer.secho(f" 🚀 sigla :: {msg}", fg="red")
    else:
        raise ValueError(f"Unknown log type: {kind}")


def load_module(module_name, module_path):
    loader = importlib.machinery.SourceFileLoader(module_name, module_path)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module


def load_filters_from(module_path):
    with suppress(FileNotFoundError):
        return load_module("filters", module_path).filters.get_filters()


def get_filters_file_content():
    return textwrap.dedent(
        """
        \"\"\"
        Export filters to use on the templates using the `FILTERS` variable
        \"\"\"
        import json
        from sigla.cli.filters import filters

        @filters.register('dump')
        def dump(var):
            return json.dumps(var, indent=4)

        """
    )


def get_definition_file_content(name):
    return textwrap.dedent(
        f"""\
            <buffer>
                <file to="output/{name}.txt">
                    <{name}>
                        [...]
                    </{name}>
                </file>
            </buffer>
        """
    )
