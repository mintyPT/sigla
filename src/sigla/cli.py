import click
from sigla import __version__
from sigla.lib.SnapshotCli import SnapshotCli, SNAPSHOTS_DIRECTORY
from sigla.lib.helpers.files import ensure_dir
from sigla.main import run

import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        # logging.StreamHandler()
    ]
)


# @click.option("--debug/--no-debug", default=False)
# click.echo('Debug mode is %s' % ('on' if debug else 'off'))
@click.group()
def cli():
    pass


@cli.command()  # @cli, not @click!
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def render(files):
    for file in files:
        run(file)


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
