from pathlib import Path

import typer

from sigla import __version__, config
from sigla.cli.definition_file import DefinitionFile
from sigla.cli.helpers import (get_definition_file_content,
                               get_filters_file_content, load_filters_from,
                               log)
from sigla.helpers import ensure_dirs
from sigla.template_loaders.file_template_loader import FileTemplateLoader

app = typer.Typer()

DEFAULT_DEFINITION_FILE = "./sigla.xml"
DEFAULT_FILTERS_FILE = "./.sigla/filters.py"
DEFAULT_TEMPLATE_DIRECTORY = "./.sigla/templates"


@app.command()
def init():
    """
    Creates all the files and folders needed to work with sigla
    """

    log("Initializing sigla folder")

    log(f"Create folder: {config.path.templates}")
    ensure_dirs(config.path.templates)

    log(f"Create folder: {config.path.snapshots}")
    ensure_dirs(config.path.snapshots)

    log(f"Create folder: {config.path.scripts}")
    ensure_dirs(config.path.scripts)

    log(f"Check/create file: {config.path.filters}")
    filepath = Path(config.path.root_directory).joinpath(
        config.path.filters_filename
    )
    if filepath.exists():
        log(f"File {filepath} already exists", kind="error")
        raise typer.Exit(code=1)
    filepath.write_text(get_filters_file_content())


@app.command()
def new_definition(name: str = DEFAULT_DEFINITION_FILE):
    """
    Will create a new definition file. Default location: ./sigla.yml
    """

    df = DefinitionFile(name)

    if not df.exists():
        log(f"File {df.filepath} already exists", kind="error")
        raise typer.Exit(code=1)

    log(f"Create definition file: {df.filepath}")
    content = get_definition_file_content(name)
    df.write(content)


@app.command()
def run(
    name: str = DEFAULT_DEFINITION_FILE,
    template_directory: str = DEFAULT_TEMPLATE_DIRECTORY,
    filters_file: str = DEFAULT_FILTERS_FILE,
):
    """
    Will run the code generation defined in a config file
    """
    df = DefinitionFile(name)
    if not df.exists():
        log(f"No definition(s) found for {df.filepath}", kind="error")
        raise typer.Exit(code=1)

    loader = FileTemplateLoader(template_directory)
    filters = load_filters_from(filters_file)

    df.generate(loader, filters=filters)


@app.command()
def version():
    """
    Print the version
    """
    log(f"Version: {__version__}")


if __name__ == "__main__":
    app()
