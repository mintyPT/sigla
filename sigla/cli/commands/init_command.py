import textwrap
from pathlib import Path

from sigla import config
from sigla.utils import ensure_dirs


def get_content():
    return textwrap.dedent(
        """
        \"\"\"
        Export filters to use on the templates using the `FILTERS` variable
        \"\"\"
        import json
        from sigla.filters import *

        @register_filter('dump')
        def dump(var):
            return json.dumps(var, indent=4)

        """
    )


def init_command():
    print(":: sigla init")
    print(f":: - checking/creating folder {config.path.templates}")
    print(f":: - checking/creating folder {config.path.snapshots}")
    print(f":: - checking/creating folder {config.path.definitions}")

    ensure_dirs(
        config.path.templates,
        config.path.snapshots,
        config.path.definitions,
    )

    print(f":: - checking/creating file {config.path.filters}")
    filters_path = Path(config.path.filters)
    filters_file_exists = filters_path.exists()
    if not filters_file_exists:
        filters_path.write_text(get_content())
