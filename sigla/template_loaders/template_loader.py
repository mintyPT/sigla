from abc import ABC, abstractmethod


# TODO Should not concern itself if tag and bundle. Only path
class TemplateLoader(ABC):
    @abstractmethod
    def load(self, tag, *, bundle=None):
        """
        This should load the "raw" template
        """
        pass

    @abstractmethod
    def write(self, content, tag, *, bundle=None):
        """
        This should load the "raw" template
        """
        pass
