from typing import Callable, Dict, Any


class FilterCollector:
    filters: Dict[str, Callable[[Any], Any]]

    def __init__(self) -> None:
        self.filters = {}

    def register(self, name: str) -> Callable[[Any], Any]:
        def wraps(f: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self.filters[name] = f
            return f

        return wraps

    def get_filters(self) -> Dict[str, Callable[[Any], Any]]:
        return self.filters
