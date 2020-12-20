import click
from sigla import __version__
from sigla.main import run


# @click.option("--debug/--no-debug", default=False)
# click.echo('Debug mode is %s' % ('on' if debug else 'off'))
@click.group()
def cli():
    pass


@cli.command()  # @cli, not @click!
@click.argument("files", nargs=-1)
def render(files):
    for file in files:
        run(file)


@cli.command()
def version():
    click.echo(f"Version: {__version__}")


if __name__ == "__main__":
    cli()
