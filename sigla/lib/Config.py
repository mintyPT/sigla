import configparser
from os.path import join

import os
from typing import Optional

BASE_PATH = os.getcwd()


class Config(configparser.ConfigParser):
    base_path: Optional[str] = None
    sigma_path: Optional[str] = None
    config_filename: Optional[str] = None

    def __init__(
        self,
        sigma_path=".sigla",
        config_filename="config.ini",
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.base_path = BASE_PATH
        self.sigma_path = join(self.base_path, sigma_path)
        self.config_filename = config_filename

        self.read(self.config_path)

        #
        # sigla
        #
        if not self.has_section("sigla"):
            self["sigla"] = {}

        self["sigla"]["templates"] = self["sigla"].get(
            "templates", ".sigla/templates"
        )
        self["sigla"]["snapshots"] = self["sigla"].get(
            "snapshots", ".sigla/snapshots"
        )
        self["sigla"]["definitions"] = self["sigla"].get(
            "definitions", ".sigla/definitions"
        )
        self["sigla"]["filters"] = self["sigla"].get(
            "filters", ".sigla/filters.py"
        )

        #
        # templates
        #
        if not self.has_section("templates"):
            self["templates"] = {}

        self["templates"]["create_missing_templates"] = str(
            self.create_missing_templates
        )

    @property
    def create_missing_templates(self):
        return self["templates"].getboolean(
            "create_missing_templates", fallback=True
        )

    @property
    def config_path(self):
        return os.path.join(self.sigma_path, self.config_filename)

    @property
    def templates_path(self):
        return join(self.base_path, self["sigla"]["templates"])

    @property
    def definitions_path(self):
        return join(self.base_path, self["sigla"]["definitions"])

    @property
    def snapshots_path(self):
        return join(self.base_path, self["sigla"]["snapshots"])

    @property
    def filters_path(self):
        return join(self.base_path, self["sigla"]["filters"])

    def save(self):
        with open(self.config_path, "w") as configfile:
            self.write(configfile)
