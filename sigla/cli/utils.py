import importlib.machinery
import types
from os.path import join

from sigla.cli.constants import get_default_template_content
from sigla.lib2.nodes.NodeTemplate import NodeTemplate


def load_module(module_name, module_path):
    loader = importlib.machinery.SourceFileLoader(module_name, module_path)
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module


def load_filters_from(module_path):
    filters = {}
    module_name = "filters"
    try:
        filters_module = load_module(module_name, module_path)
        if "FILTERS" in dir(filters_module):
            filters = filters_module.FILTERS
    except FileNotFoundError:
        pass
    return filters


def write_file(p, content):
    with open(p, "w") as h:
        h.write(content)


def read_file(p):
    with open(p, "r") as h:
        return h.read()


def cliNodeTemplateFactory(_path):
    class CliNodeTemplate(NodeTemplate):
        def __init__(self, tag, attributes=None):
            super().__init__(tag, attributes)

        def raw_template_loader(self, tag) -> str:
            template_path = join(_path, f"{tag}.jinja2")
            try:
                return read_file(template_path)
            except FileNotFoundError:
                content = get_default_template_content(self.get_data_for_template())
                write_file(template_path, content)
                return content

    return CliNodeTemplate