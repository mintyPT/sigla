import os
from pathlib import Path

import typer
from rich.traceback import install

from sigla import __version__
from sigla.cli.definition_file.definition_file import DefinitionFile
from sigla.cli.helpers import (
    get_definition_file_content,
    get_filters_file_content,
    load_filters_from,
    log,
)
from sigla.config import config
from sigla.data.data_loaders.xml_to_data import convert_xml_string_to_data
from sigla.engines.engines import SiglaEngine
from sigla.helpers.helpers import ensure_dirs
from sigla.template_loaders.template_loaders import FileTemplateLoader

app = typer.Typer()

CWD = Path(os.getcwd())

DEFAULT_DEFINITION_FILE = "sigla.xml"
DEFAULT_FILTERS_FILE = ".sigla/filters.py"
DEFAULT_TEMPLATE_DIRECTORY = ".sigla/templates"

install()


@app.command()
def init() -> None:
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
def new_definition(name: str = DEFAULT_DEFINITION_FILE) -> None:
    """
    Will create a new definition file. Default location: ./sigla.yml
    """
    name = CWD.joinpath(name)

    df = DefinitionFile(name)

    if df.exists():
        log(f"File {df.filepath} already exists", kind="error")
        raise typer.Exit(code=1)

    log(f"Create definition file: {df.filepath}")
    content = get_definition_file_content(name)
    df.write(content)


@app.command()
def run(
    name: str = DEFAULT_DEFINITION_FILE,
    template_loader_directory: str = DEFAULT_TEMPLATE_DIRECTORY,
    filters_file: str = DEFAULT_FILTERS_FILE,
) -> None:
    """
    Will run the code generation defined in a config file
    """
    name = CWD.joinpath(name)

    df = DefinitionFile(name)
    if not df.exists():
        log(f"No definition(s) found for {df.filepath}", kind="error")
        raise typer.Exit(code=1)

    template_loader_directory = CWD.joinpath(template_loader_directory)
    template_loader = FileTemplateLoader(template_loader_directory)

    filters_file = CWD.joinpath(filters_file)
    filters = load_filters_from(filters_file)

    xml = df.read()
    data = convert_xml_string_to_data(xml)
    SiglaEngine.generate(data, template_loader, filters=filters)


@app.command()
def version() -> None:
    """
    Print the version
    """
    log(f"Version: {__version__}")


if __name__ == "__main__":
    app()
