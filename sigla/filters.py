FILTERS = {}


def register_filter(name):
    def wraps(f):
        FILTERS[name] = f
        return f

    return wraps