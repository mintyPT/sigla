import json


def cast_property(name, value):
    casters = {
        "int": int,
        "float": float,
        "json": json.loads,
        "bool": lambda v: v.lower() in ["true", "1"],
    }
    for kind, caster in casters.items():
        dashed_kind = "-" + kind
        if name.endswith(dashed_kind):
            new_key = name.replace(dashed_kind, "")
            new_value = caster(value)
            return new_key, new_value

    return name, value


def cast_dict(attributes: dict) -> dict:
    """
    Takes a dict of props and casts them if necessary
    """
    ret = {}
    for name, value in attributes.items():
        name, value = cast_property(name, value)
        ret[name] = value
    return ret
