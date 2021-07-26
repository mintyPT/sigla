class FilterCollector:
    def __init__(self):
        self.filters = {}

    def register(self, name):
        def wraps(f):
            self.filters[name] = f
            return f

        return wraps

    def get_filters(self):
        return self.filters
