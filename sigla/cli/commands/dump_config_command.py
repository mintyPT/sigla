from sigla import config


def dump_config_command():
    print(f"|> config.path.templates:\t {config.path.templates}")
    print(f"|> config.path.snapshots:\t {config.path.snapshots}")
    print(f"|> config.path.definitions:\t {config.path.definitions}")
    print(f"|> config.path.filters:\t {config.path.filters}")
    print("")
    print(f"|> config.cls.node_list:\t {config.cls.node_list}")
