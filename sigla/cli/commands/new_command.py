import textwrap
from pathlib import Path

import typer

from sigla import config


def get_content(name):
    return textwrap.dedent(
        f"""\
        <root>
            <file to="output/{name}[.ext]">
                <{name}>
                    [...]
                </{name}>
            </file>
        </root>
    """
    )


def new_command(name):
    print(f":: creating new definition: {name}")

    destination = Path(config.path.definitions).joinpath(f"{name}.xml")

    if destination.exists():
        raise typer.Exit("✋ This definition already exists")

    destination.write_text(get_content(name))
