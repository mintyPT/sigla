#!/usr/bin/python

import click
import os
from shutil import copyfile
import xml.etree.ElementTree as ET


@click.command()
@click.argument("definition", type=click.Path(exists=True))
@click.option("--test", is_flag=True)
@click.option("--make", is_flag=True)
def main(test, make, definition):
    is_making = make
    xml_file = definition

    doc = ET.parse(xml_file).getroot()
    kgdir = doc.attrib["kgdir"]
    if not kgdir:
        print("No known good directory defined on the 'ut' tag.\n")

    # Go through the XML nodes and pull out all of the tests
    tests = []
    for test_node in doc.iter("test"):
        files = []
        files.append(test_node.attrib["out"])

        for out_node in test_node.iter("out"):
            out = out_node.text.strip()
            files.append(out)

        tests.append({"command": test_node.attrib["cmd"], "output_files": files})

    # Iterate through the tests and execute them
    failures = []

    for test in tests:
        print(test["command"])
        r = os.system(test["command"])
        # r = subprocess.run(test['command'].split(' '))

        for file in test["output_files"]:
            known_good_name = kgdir + "/" + file

            with open(file, "r") as h:
                current_result = h.read()

            if is_making:
                print(f"Storing {file} to {known_good_name}\n")
                copyfile(file, known_good_name)
                print(f"Known good {known_good_name} stored\n")
            else:
                # print(f"Checking {file} against {known_good_name}")

                with open(known_good_name, "r") as h:
                    good_result = h.read()

                if good_result != current_result:
                    print("Failure: Known good comparison failed\n")
                    failures.append(test.command)

    if is_making == False:
        if len(failures) > 0:
            print("\n\nTests failed:\n\n")
            for test in failures:
                print(f"  {test}\n")
        else:
            print("\n\nNo test failures\n")


if __name__ == "__main__":
    main()
