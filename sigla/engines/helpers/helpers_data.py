from sigla.data.data import Data


def get_template_path(data: Data, extension: str = "jinja2") -> str:
    if bundle := data.get("bundle"):
        result = f"{bundle}/{data.tag}.{extension}"
    else:
        result = f"{data.tag}.{extension}"
    return result
