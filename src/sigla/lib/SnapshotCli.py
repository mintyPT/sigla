import os
from shutil import copyfile

from sigla.lib.helpers.files import ensure_parent_dir, ensure_dir
from sigla.lib.helpers.loaders import load_xml

SNAPSHOTS_DIRECTORY = '.sigla/snapshots'


class SnapshotCli:
    def __init__(self, file):
        print(f":: Loading {file}")
        self.doc = load_xml(file)

        print(f":: Ensure {SNAPSHOTS_DIRECTORY} exists")
        ensure_dir(SNAPSHOTS_DIRECTORY)

        print(f":: Reading tests")
        self.tests = []
        for test_node in self.doc.iter("test"):
            files = [test_node.attrib["out"]]

            for out_node in test_node.iter("out"):
                out = out_node.text.strip()
                files.append(out)

            self.tests.append({"command": test_node.attrib["cmd"], "output_files": files})
        print(f'    ‣ Loaded {len(self.tests)} commands')

    def make_snapshots(self):
        print(f":: Making snapshots")
        for test in self.tests:
            print(f'    ‣ Command {test["command"]}')
            os.system(test["command"])

            for file in test["output_files"]:
                known_good_name = SNAPSHOTS_DIRECTORY + "/" + file

                with open(file, "r") as h:
                    current_result = h.read()

                #
                # MAKING
                #
                ensure_parent_dir(known_good_name)
                print(f"        ‣ Saving snapshot {file} to {known_good_name}")
                copyfile(file, known_good_name)

    def verify_snapshots(self):
        print(f":: Making snapshots")
        failures = []
        for test in self.tests:
            print(f'    ‣ Command {test["command"]}')
            os.system(test["command"])

            for file in test["output_files"]:
                known_good_name = SNAPSHOTS_DIRECTORY + "/" + file

                with open(file, "r") as h:
                    current_result = h.read()

                #
                # TESTING
                #
                print(f"        ‣ Checking snapshot {file} against {known_good_name}")
                with open(known_good_name, "r") as h:
                    good_result = h.read()

                if good_result != current_result:
                    print("        🚩 Snapshot comparison failed")
                    failures.append(test['command'])
