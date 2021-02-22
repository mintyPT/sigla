from typing import List

import typer
import environ
from pathlib import Path

from cli.cli_utils import cli_new_definition, cli_run_definitions
from core import ensure_dirs, __version__
from cli.constants import filter_file_default_content

app = typer.Typer()


@environ.config(prefix="")
class CliConfig:
    @environ.config
    class Paths:
        templates = environ.var(".core/templates")
        snapshots = environ.var(".core/snapshots")
        definitions = environ.var(".core/definitions")
        filters = environ.var(".core/filters.py")

    path = environ.group(Paths)


cfg = environ.to_config(CliConfig)


@app.command()
def dump_config():
    print(f"|> path.templates:\t {cfg.path.templates}")
    print(f"|> path.snapshots:\t {cfg.path.snapshots}")
    print(f"|> path.definitions:\t {cfg.path.definitions}")
    print(f"|> path.filters:\t {cfg.path.filters}")


@app.command()
def init():
    """
    Creates the .init folder to keep stuff
    """
    print(":: 💨 core init")
    print(f":: - checking/creating folder {cfg.path.templates}")
    print(f":: - checking/creating folder {cfg.path.snapshots}")
    print(f":: - checking/creating folder {cfg.path.definitions}")
    ensure_dirs(
        cfg.path.templates,
        cfg.path.snapshots,
        cfg.path.definitions,
    )

    filter_file = cfg.path.filters
    print(f":: - checking/creating file {filter_file}")
    # create file if it does not exist
    if Path(filter_file).exists():
        return
    with open(filter_file, "w") as h:
        h.write(filter_file_default_content)


@app.command()
def new(name: str):
    """
    Generate a new definition for a generator.
    """
    print(f":: creating new definition: {name}")
    destination_folder = cfg.path.definitions
    cli_new_definition(destination_folder, name)


@app.command()
def run(references: List[str]):
    """
    Run a generator
    """
    cli_run_definitions(cfg.path.definitions, references)


@app.command()
def version():
    """
    Print the version
    """

    print(f"Version: {__version__}")


if __name__ == "__main__":
    app()

# import textwrap
# from pathlib import Path
# from pprint import pformat
# import click
# from core import __version__

# # @click.option("--debug/--no-debug", default=False)
# # click.echo('Debug mode is %s' % ('on' if debug else 'off'))
# @click.group()
# @pass_config
# def cli(config: CliConfig):
#     print("=== core ===")
#     config.load()
#     print(f":: config\n{pformat(config, indent=1)}")
#     print("")
#     config.save()
#


#
#

#
#

#
#
# @cli.command()
# @click.argument("files", nargs=-1, type=click.Path(exists=True))
# def snapshot(files):
#     """
#     Makes snapshots
#     """
#     for file in files:
#         cli_make_snapshots(cli_read_snapshot_definition(file))
#
#
# @cli.command()
# @click.argument("files", nargs=-1, type=click.Path(exists=True))
# def verify(files):
#     """
#     Verify snapshots
#     """
#     for file in files:
#         cli_verify_snapshots(cli_read_snapshot_definition(file))
#
#
# if __name__ == "__main__":
#     cli()
