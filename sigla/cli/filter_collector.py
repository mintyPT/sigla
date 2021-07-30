from typing import Callable, Dict


class FilterCollector:
    def __init__(self) -> None:
        self.filters = {}

    def register(self, name: str) -> Callable:
        def wraps(f: Callable) -> Callable:
            self.filters[name] = f
            return f

        return wraps

    def get_filters(self) -> Dict:
        return self.filters
