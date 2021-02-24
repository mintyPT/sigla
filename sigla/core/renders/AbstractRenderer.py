import abc


class AbstractRenderer(abc.ABC):
    @abc.abstractmethod
    def render(self, tpl: str, filters: dict, **kwargs: any) -> str:
        pass
