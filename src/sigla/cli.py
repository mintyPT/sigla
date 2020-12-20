import click
from sigla import process_node
from sigla.lib.SiglaFile import SiglaFile
from sigla.lib.helpers.loaders import load_xml


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    # click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    pass


# @cli.command()  # @cli, not @click!
# def init():
#     click.echo('Syncing')


@cli.command()  # @cli, not @click!
@click.argument("files", nargs=-1)
def render(files):
    for file in files:

        root = load_xml(file)

        result = process_node(root)

        for r in result:
            if type(r) == SiglaFile:
                print(f"|> Saving to {r.path}")
                r.save("output")
            elif type(r) == str:
                print(r)
            else:
                raise NotImplementedError(
                    f"No final handling implemented for {type(r)}"
                )


if __name__ == "__main__":
    cli()
