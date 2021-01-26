from pprint import pformat
import click
from sigla import __version__
from sigla.classes.Config import CliConfig
from sigla.helpers.cli import (
    cli_new_definition,
    cli_run_definitions,
    cli_read_snapshot_definition,
    cli_make_snapshots,
    cli_verify_snapshots,
)
from sigla.constants import filter_file_template
from sigla.helpers.files import ensure_dirs, ensure_file

pass_config = click.make_pass_decorator(CliConfig, ensure=True)


# @click.option("--debug/--no-debug", default=False)
# click.echo('Debug mode is %s' % ('on' if debug else 'off'))
@click.group()
@pass_config
def cli(config: CliConfig):
    print("=== sigla ===")
    config.load()
    print(f":: config\n{pformat(config, indent=1)}")
    print("")
    config.save()


@cli.command()
@pass_config
def init(config):
    """
    Every project needs a home. Creates the folders and files necessary
    """
    print(f":: checking/creating folder {config['path_templates']}")
    print(f":: checking/creating folder {config['path_snapshots']}")
    print(f":: checking/creating folder {config['path_definitions']}")
    ensure_dirs(
        config["path_templates"],
        config["path_snapshots"],
        config["path_definitions"],
    )
    #
    filter_file = config["path_filters"]
    print(f":: checking/creating file {filter_file}")
    ensure_file(filter_file, filter_file_template)


@cli.command()
def version():
    """
    Print the version
    """
    click.echo(f"Version: {__version__}")


@cli.command()
@pass_config
@click.argument("name", type=click.types.STRING)
def nd(config, name):
    """
    Will generate a new definition (nd) file inside your definitions
    folder. This file is used to add data/variables to generate code.
    """
    print(f":: creating new definition: {name}")
    destination_folder = config["path_definitions"]
    ensure_dirs(destination_folder)
    cli_new_definition(destination_folder, name)


@cli.command()
@pass_config
@click.argument("references", nargs=-1, type=click.types.STRING)
def rd(config: CliConfig, references):
    """
    Run a definition (rd) file to generate files from templates
    """
    cli_run_definitions(config, references)


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def snapshot(files):
    """
    Makes snapshots
    """
    for file in files:
        cli_make_snapshots(cli_read_snapshot_definition(file))


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def verify(files):
    """
    Verify snapshots
    """
    for file in files:
        cli_verify_snapshots(cli_read_snapshot_definition(file))


if __name__ == "__main__":
    cli()
