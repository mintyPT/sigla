import pydash as _


def get_nested(arr, field):
    return map(lambda el: _.get(el, field), arr)