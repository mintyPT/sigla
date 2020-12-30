import json


def dump(var):
    return json.dumps(var, indent=4)


FILTERS = {"dump": dump}
