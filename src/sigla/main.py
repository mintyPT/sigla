import click
from sigla.lib.Node import Node
from sigla.lib.Processor import Processor
from sigla.lib.SiglaFile import SiglaFile
from sigla.lib.utils import load_xml, cast_array


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    # click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    pass


# @cli.command()  # @cli, not @click!
# def init():
#     click.echo('Syncing')


@cli.command()  # @cli, not @click!
@click.argument('files', nargs=-1)
def render(files):
    for file in files:

        processor = Processor()

        root = load_xml(file)
        node = Node.from_xml(root)

        result = processor.process_node(node)
        result = cast_array(result)

        for r in result:
            if type(r) == SiglaFile:
                print(f'|> Saving to {r.path}')
                r.save('output')
            elif type(r) == str:
                print(r)
            else:
                raise NotImplementedError(f"No final handling implemented for {type(r)}")


if __name__ == '__main__':
    cli()
