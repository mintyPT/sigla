import os
from shutil import copyfile

from sigla.lib.helpers.files import ensure_parent_dir, ensure_dirs
from sigla.lib.helpers.loaders import load_xml

SNAPSHOTS_DIRECTORY = ".sigla/snapshots"


class SnapshotCli:
    def __init__(self, file):
        print(f":: Loading {file}")
        self.doc = load_xml(file)

        print(f":: Ensure {SNAPSHOTS_DIRECTORY} exists")
        ensure_dirs(SNAPSHOTS_DIRECTORY)

        print(":: Reading tests")
        self.tests = []
        for test_node in self.doc.iter("test"):
            files = [test_node.attrib["out"]]

            for out_node in test_node.iter("out"):
                out = out_node.text.strip()
                files.append(out)

            self.tests.append(
                {"command": test_node.attrib["cmd"], "output_files": files}
            )
        print(f"    ‣ Loaded {len(self.tests)} commands")

    def make_snapshots(self):
        print(":: Making snapshots")
        for test in self.tests:
            print(f'    ‣ Command {test["command"]}')
            os.system(test["command"])

            for file in test["output_files"]:
                gn = SNAPSHOTS_DIRECTORY + "/" + file

                #
                # MAKING
                #
                ensure_parent_dir(gn)
                print(f"        ‣ Saving snapshot {file} to {gn}")
                copyfile(file, gn)

    def verify_snapshots(self):
        print(":: Making snapshots")
        failures = []
        for test in self.tests:
            print(f'    ‣ Command {test["command"]}')
            os.system(test["command"])

            for file in test["output_files"]:
                gn = SNAPSHOTS_DIRECTORY + "/" + file

                with open(file, "r") as h:
                    current_result = h.read()

                #
                # TESTING
                #
                print(f"        ‣ Checking snapshot {file} against {gn}")
                with open(gn, "r") as h:
                    good_result = h.read()

                if good_result != current_result:
                    print("        🚩 Snapshot comparison failed")
                    failures.append(test["command"])
