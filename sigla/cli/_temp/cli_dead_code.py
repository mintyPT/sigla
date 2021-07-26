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
#     log(f":: Loading {file}")
#     doc = load_xml_from_file(file)
#     log(f":: Ensure {SNAPSHOTS_DIRECTORY} exists")
#     ensure_dirs(SNAPSHOTS_DIRECTORY)
#     log(":: Reading tests")
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
#     log(f"    ‣ Loaded {len(tests)} commands")
#     return tests
#
#
# def cli_make_snapshots(tests):
#     log(":: Making snapshots")
#     for test in tests:
#         log(f'    ‣ Command {test["command"]}')
#         os.system(test["command"])
#
#         for file in test["output_files"]:
#             gn = SNAPSHOTS_DIRECTORY + "/" + file
#
#             #
#             # MAKING
#             #
#             ensure_parent_dir(gn)
#             log(f"        ‣ Saving snapshot {file} to {gn}")
#             copyfile(file, gn)
#
#
# def cli_verify_snapshots(tests):
#     log(":: Checking snapshots")
#     failures = []
#     for test in tests:
#         log(f'    ‣ Command {test["command"]}')
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
#             log(f"        ‣ Checking snapshot {file} against {gn}")
#             with open(gn, "r") as h:
#                 good_result = h.read()
#
#             if good_result != current_result:
#                 log("        🚩 Snapshot comparison failed")
#                 failures.append(test["command"])
