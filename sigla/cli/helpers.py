import textwrap
from contextlib import suppress

import typer

from helpers.helpers import load_module


def log(msg: str, kind: str = "default") -> None:
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


def load_filters_from(module_path: str) -> dict:
    with suppress(FileNotFoundError):
        return load_module("filters", str(module_path)).filters.get_filters()
    return {}


def get_filters_file_content() -> str:
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


def get_definition_file_content(name: str) -> str:
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
