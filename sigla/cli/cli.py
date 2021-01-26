from pprint import pformat

import click
from os.path import join
from pathlib import Path
from sigla import __version__
from sigla.classes.Config import CliConfig
from sigla.cli.constants import filter_file_template, new_definition_template
from sigla.cli.utils import (
    write_file,
    read_file,
    cliNodeTemplateFactory,
)
from sigla.helpers.files import ensure_dirs, ensure_file
from sigla.lib.errors import TemplateDoesNotExistError
from sigla.lib.funcs import import_from_xml_string
from sigla.lib.outputs.FileOutput import FileOutput
from sigla.classes.SnapshotCli import SnapshotCli

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
    dirs = (
        config["path_templates"],
        config["path_snapshots"],
        config["path_definitions"],
    )
    filter_file = config["path_filters"]

    for d in dirs:
        print(f":: checking/creating folder {d}")
    print(f":: checking/creating file {filter_file}")

    ensure_dirs(*dirs)
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
    path_ = join(config["path_definitions"], name + ".xml")
    print(f":: creating file {path_}")

    p = Path(path_)
    p.parent.mkdir(parents=True, exist_ok=True)

    if p.exists():
        print("✋ This definition already exists")
        return

    # if file exists throw error
    content = new_definition_template(name)
    write_file(p, content)


#
#
#
#


@cli.command()
@pass_config
@click.argument("references", nargs=-1, type=click.types.STRING)
def rd(config: CliConfig, references):
    """
    Run a definition (rd) file to generate files from templates
    """

    for reference in references:
        glob = Path(config["path_definitions"]).glob(f"{reference}.xml")
        for p in glob:
            if not p.exists():
                print("✋ This definition does not exists")
                return
            if p.is_dir():
                continue

            try:
                print(f":: Reading {p}")
                str_xml = read_file(p)
                stuff = import_from_xml_string(
                    str_xml, TemplateClass=cliNodeTemplateFactory(config)
                ).process()

                for s in stuff:
                    if isinstance(s, FileOutput):
                        print(f":: Saving {s.path}")
                        s.save()
                    else:
                        print("\n" * 1)
                        print(":: template to output")
                        print(s.content)
            except TemplateDoesNotExistError as e:
                print("|> e", e)
                raise Exception()


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
