import click
import textwrap
from os.path import join
from pathlib import Path
from sigla import __version__
from sigla.cli.utils import load_filters_from
from sigla.lib.helpers.files import ensure_dirs, ensure_file
from sigla.main import run
from sigla.lib.Config import Config
from sigla.cli.SnapshotCli import SnapshotCli


class SiglaConfig(Config):
    config: Path = Path.cwd().joinpath(".sigla/config.json")
    defaults = {
        "path_templates": ".sigla/templates",
        "path_snapshots": ".sigla/snapshots",
        "path_definitions": ".sigla/definitions",
        "path_filters": ".sigla/filters.py",
    }


pass_config = click.make_pass_decorator(SiglaConfig, ensure=True)


# @click.option("--debug/--no-debug", default=False)
# click.echo('Debug mode is %s' % ('on' if debug else 'off'))
@click.group()
@pass_config
def cli(config):
    config.load()


@cli.command()
@pass_config
def init(config):
    ensure_dirs(
        config["path_templates"],
        config["path_snapshots"],
        config["path_definitions"],
    )
    DEFAULT_FILTERS_FILE_CONTENT = textwrap.dedent(
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

    ensure_file(config["path_filters"], DEFAULT_FILTERS_FILE_CONTENT)
    config.save()


@cli.command()
@pass_config
@click.argument("name", type=click.types.STRING)
def new_definition(config, name):
    p = Path(join(config["path_definitions"], name + ".xml"))
    p.parent.mkdir(parents=True, exist_ok=True)

    if p.exists():
        raise Exception("This definition already exists")

    name = name.replace("/", "-")

    # if file exists throw error
    with open(p, "w") as h:
        h.write(textwrap.dedent(
            f"""\
                <root>
                    <file name="output/{name}[.ext]">
                        <{name}>
                            [...]
                        </{name}>
                    </file>
                </root>
            """
        ))


@cli.command()
@pass_config
@click.argument("references", nargs=-1, type=click.types.STRING)
def run_definition(config, references):
    filters = load_filters_from(config["path_filters"])

    for reference in references:
        glob = Path(config["path_definitions"]).glob(f"{reference}.xml")
        for p in glob:
            if not p.exists():
                raise Exception("This definition does not exists")
            if p.is_dir():
                continue
            run(file=p, filters=filters)
        return


# @cli.command()  # @cli, not @click!
# @click.argument("files", nargs=-1, type=click.Path(exists=True))
# def render(files):
#     for file in files:
#         run(file=file)


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
