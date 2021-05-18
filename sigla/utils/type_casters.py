import json

casters = {
    "int": int,
    "float": float,
    "json": json.loads,
    "bool": lambda v: v.lower() in ["true", "1"],
}


def cast_property(prop_name, prop_value):
    for kind, caster in casters.items():
        dashed_kind = "-" + kind
        if prop_name.endswith(dashed_kind):
            new_key = prop_name.replace(dashed_kind, "")
            new_value = caster(prop_value)
            return new_key, new_value

    return prop_name, prop_value
