from os.path import join

from sigla.classes.Config import CliConfig
from sigla.classes.nodes.NodeTemplate import NodeTemplate
from sigla.constants import get_default_template_content
from sigla.helpers.files import read_file, write_file
from sigla.helpers.modules import load_filters_from


def CliEntityConfigFactory(config: CliConfig):
    class CliNodeTemplate(NodeTemplate):
        def __init__(self, tag, attributes=None):
            super().__init__(tag, attributes)

        def get_filters(self):
            filters = load_filters_from(config["path_filters"])
            return filters

        def raw_template_loader(self, tag) -> str:
            template_path = join(config["path_templates"], f"{tag}.jinja2")
            try:
                return read_file(template_path)
            except FileNotFoundError:
                content = get_default_template_content(
                    self.get_data_for_template()
                )
                write_file(template_path, content)
                return content

    return CliNodeTemplate