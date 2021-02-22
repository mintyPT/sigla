import os
import textwrap
from os.path import join
from pathlib import Path
from shutil import copyfile

import typer
from core import ensure_dirs
from core.errors import TemplateDoesNotExistError
from core.outputs.OutputFile import OutputFile
from core.importers import import_from_xml_string
from core import load_xml_from_file


def new_definition_template(name):
    return textwrap.dedent(
        f"""\
    <root>
        <file to="output/{name}[.ext]">
            <{name}>
                [...]
            </{name}>
        </file>
    </root>
"""
    )


def cli_new_definition(folder, name, get_template=new_definition_template):
    destination = join(folder, name + ".xml")

    p = Path(destination)
    if p.exists():
        raise Exception("✋ This definition already exists")

    content = get_template(name)
    with open(p, "w") as h:
        h.write(content)


def cli_run_definition(p):
    print(f":: Reading {p}")

    with open(p, "r") as h:
        str_xml = h.read()

    print("|> before stuff")

    stuff = import_from_xml_string(str_xml)()
    print("|> stuff", stuff)

    for s in stuff:
        if isinstance(s, OutputFile):
            print(f":: Saving {s.path}")
            s.save()
        else:
            print("\n" * 1)
            print(":: template to output")
            print(s.content)


def cli_run_definitions(path, references):
    for reference in references:
        glob = Path(path).glob(f"{reference}.xml")

        c = 0
        for p in glob:
            c += 1
            if not p.exists():
                raise typer.Exit(f"✋ The definition(s) do not exists {p}")

            if p.is_dir():
                continue

            try:
                cli_run_definition(p)
            except TemplateDoesNotExistError as e:
                print("|> e", e)
                raise Exception()
                raise typer.Exit(e)

        if c == 0:
            raise typer.Exit(f"✋ The definition(s) do not exists {references}")


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
            ensure_dirs(Path(gn).parent)
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


SNAPSHOTS_DIRECTORY = ".core/snapshots"
