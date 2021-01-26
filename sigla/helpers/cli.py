import os
from os.path import join
from pathlib import Path
from shutil import copyfile

from sigla.classes.CliEntityConfigFactory import CliEntityConfigFactory
from sigla.classes.errors import TemplateDoesNotExistError
from sigla.classes.outputs.FileOutput import FileOutput

from sigla.constants import new_definition_template
from sigla.helpers.files import (
    ensure_dirs,
    write,
    read,
    ensure_parent_dir,
)
from sigla.helpers.importers import import_from_xml_string
from sigla.helpers.xml import load_xml_from_file


def cli_new_definition(
    folder, name, write=write, get_template=new_definition_template
):
    destination = join(folder, name + ".xml")

    p = Path(destination)
    if p.exists():
        raise Exception("✋ This definition already exists")

    content = get_template(name)
    write(p, content)


def cli_run_definition(config, p):
    print(f":: Reading {p}")
    str_xml = read(p)
    stuff = import_from_xml_string(
        str_xml, TemplateClass=CliEntityConfigFactory(config)
    ).process()
    for s in stuff:
        if isinstance(s, FileOutput):
            print(f":: Saving {s.path}")
            s.save()
        else:
            print("\n" * 1)
            print(":: template to output")
            print(s.content)


def cli_run_definitions(config, references):
    for reference in references:
        glob = Path(config["path_definitions"]).glob(f"{reference}.xml")
        for p in glob:
            if not p.exists():
                print("✋ This definition does not exists")
                continue

            if p.is_dir():
                continue

            try:
                cli_run_definition(config, p)
            except TemplateDoesNotExistError as e:
                print("|> e", e)
                raise Exception()


def cli_read_snapshot_definition(file):
    print(f":: Loading {file}")
    doc = load_xml_from_file(file)
    print(f":: Ensure {SNAPSHOTS_DIRECTORY} exists")
    ensure_dirs(SNAPSHOTS_DIRECTORY)
    print(":: Reading tests")
    tests = []
    for test_node in doc.iter("test"):
        files = [test_node.attrib["out"]]

        for out_node in test_node.iter("out"):
            out = out_node.text.strip()
            files.append(out)

        tests.append(
            {"command": test_node.attrib["cmd"], "output_files": files}
        )
    print(f"    ‣ Loaded {len(tests)} commands")
    return tests


def cli_make_snapshots(tests):
    print(":: Making snapshots")
    for test in tests:
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


def cli_verify_snapshots(tests):
    print(":: Checking snapshots")
    failures = []
    for test in tests:
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


SNAPSHOTS_DIRECTORY = ".sigla/snapshots"
