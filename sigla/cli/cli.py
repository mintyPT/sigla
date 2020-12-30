import pretty_errors
from os.path import join
from pathlib import Path

import click

# import logging

from sigla import __version__
from sigla.lib.helpers.files import ensure_dirs, ensure_parent_dir
from sigla.main import run
from sigla.lib.Config import Config
from sigla.cli.SnapshotCli import SnapshotCli

# logging.basicConfig(
#     level=logging.INFO,
#     format="[%(levelname)s] %(message)s",
#     handlers=[
#         logging.FileHandler("debug.log"),
#         # logging.StreamHandler()
#     ],
# )

config = Config()


# @click.option("--debug/--no-debug", default=False)
# click.echo('Debug mode is %s' % ('on' if debug else 'off'))
@click.group()
def cli():
    pass


@cli.command()
def init():
    ensure_dirs(
        config.sigma_path,
        config.templates_path,
        config.snapshots_path,
        config.definitions_path,
    )
    config.save()


@cli.command()
@click.argument("name", type=click.types.STRING)
def new_definition(name):
    p = Path(join(config.definitions_path, name + ".xml"))
    ensure_parent_dir(p)
    name = name.replace("/", "-")

    if p.exists():
        raise Exception("This definition already exists")

    # if file exists throw error
    with open(p, "w") as h:
        h.write(
            f"""<root>
    <file name="output/{name}[.ext]">
        <{name}>
        </{name}>
    </file>
</root>"""
        )


@cli.command()
@click.argument("name", type=click.types.STRING)
def run_definition(name):
    p = Path(join(config.definitions_path, name + ".xml"))
    if not p.exists():
        raise Exception("This definition does not exists")
    run(file=p)


@cli.command()  # @cli, not @click!
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def render(files):
    for file in files:
        run(file=file)


@cli.command()
def version():
    """
    Prints the current version
    """
    click.echo(f"Version: {__version__}")


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def snapshot(files):
    """
    Makes snapshots
    """
    for file in files:
        snap = SnapshotCli(file)
        snap.make_snapshots()


@cli.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def verify(files):
    """
    Verify snapshots
    """
    for file in files:
        snap = SnapshotCli(file)
        snap.verify_snapshots()


if __name__ == "__main__":
    cli()
