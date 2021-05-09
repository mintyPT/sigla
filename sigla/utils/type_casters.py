import json


def cast_property(prop_name, prop_value):
    if prop_name.endswith("-int"):
        return cast_int(prop_name, prop_value)

    elif prop_name.endswith("-float"):
        return cast_float(prop_name, prop_value)

    elif prop_name.endswith("-json"):
        return cast_json(prop_name, prop_value)

    elif prop_name.endswith("-bool"):
        return cast_bool(prop_name, prop_value)

    return prop_name, prop_value


def cast_bool(prop_name, prop_value):
    new_key = prop_name.replace("-bool", "")
    new_value = True if prop_value.lower() in ["true", "1"] else False
    return new_key, new_value


def cast_json(prop_name, prop_value):
    new_key = prop_name.replace("-json", "")
    new_value = json.loads(prop_value)
    return new_key, new_value


def cast_float(prop_name, prop_value):
    new_key = prop_name.replace("-float", "")
    new_value = float(prop_value)
    return new_key, new_value


def cast_int(prop_name, prop_value):
    new_key = prop_name.replace("-int", "")
    new_value = int(prop_value)
    return new_key, new_value
