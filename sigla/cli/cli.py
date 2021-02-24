import typer
from typing import List
from sigla import __version__
from sigla.cli.commands.RunCommand import RunCommand
from sigla.cli.commands.dump_config_command import dump_config_command
from sigla.cli.commands.init_command import init_command
from sigla.cli.commands.new_command import new_command

app = typer.Typer()


@app.command()
def dump_config():
    dump_config_command()


@app.command()
def init():
    """ Creates the .init folder to keep stuff """
    init_command()


@app.command()
def new(name: str):
    """ Generate a new definition for a generator. """
    new_command(name)


@app.command()
def run(references: List[str]):
    """ run a generator """
    run_command = RunCommand(references)
    run_command()


@app.command()
def version():
    """ Print the version """
    print(f"Version: {__version__}")


if __name__ == "__main__":
    app()

# class SnapshotCommand(AbstractDefinitionBasedCommand):
#     pass
#
#
# @app.command()
# def snapshot(references: List[str]):
#     """
#     Make snapshots
#     """
#     snapshot_command = SnapshotCommand(references)
#     snapshot_command()
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
# <ut kgdir="kg">
#   <test cmd="ruby -I../lp rpcgen.rb examples/Test.java">
#     <out>examples/TestHandler.java</out>
#     <out>examples/TestStubs.java</out>
#   </test>
# </ut>
#
#
#
# def cli_read_snapshot_definition(file):
#     print(f":: Loading {file}")
#     doc = load_xml_from_file(file)
#     print(f":: Ensure {SNAPSHOTS_DIRECTORY} exists")
#     ensure_dirs(SNAPSHOTS_DIRECTORY)
#     print(":: Reading tests")
#     tests = []
#     for test_node in doc.iter("test"):
#         files = [test_node.attrib["out"]]
#
#         for out_node in test_node.iter("out"):
#             out = out_node.text.strip()
#             files.append(out)
#
#         tests.append(
#             {"command": test_node.attrib["cmd"], "output_files": files}
#         )
#     print(f"    ‣ Loaded {len(tests)} commands")
#     return tests
#
#
# def cli_make_snapshots(tests):
#     print(":: Making snapshots")
#     for test in tests:
#         print(f'    ‣ Command {test["command"]}')
#         os.system(test["command"])
#
#         for file in test["output_files"]:
#             gn = SNAPSHOTS_DIRECTORY + "/" + file
#
#             #
#             # MAKING
#             #
#             ensure_parent_dir(gn)
#             print(f"        ‣ Saving snapshot {file} to {gn}")
#             copyfile(file, gn)
#
#
# def cli_verify_snapshots(tests):
#     print(":: Checking snapshots")
#     failures = []
#     for test in tests:
#         print(f'    ‣ Command {test["command"]}')
#         os.system(test["command"])
#
#         for file in test["output_files"]:
#             gn = SNAPSHOTS_DIRECTORY + "/" + file
#
#             with open(file, "r") as h:
#                 current_result = h.read()
#
#             #
#             # TESTING
#             #
#             print(f"        ‣ Checking snapshot {file} against {gn}")
#             with open(gn, "r") as h:
#                 good_result = h.read()
#
#             if good_result != current_result:
#                 print("        🚩 Snapshot comparison failed")
#                 failures.append(test["command"])
