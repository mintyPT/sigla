import types
import importlib.machinery


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
