from pathlib import Path
from typing import Any

from sigla.nodes.node import Node
from sigla.utils.helpers import ensure_dirs

# TODO
# <models>
#   <model name="User">
#     ...
#   </model>
# </models>
# <forms>
#   <user_form model="User"
#       /or/ model-query="models model[name='User']" /or/ $model="User">
#     ...
#   </user_form>
# </forms>


class NodeFile(Node):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self.content = None

    @property
    def to(self):
        return self.data.attributes["to"]

    def process(self):
        super().process()
        self.content = self.children()
        self.validate_to_attribute()
        return self

    def validate_to_attribute(self):
        # TODO convert this to validation mechanism
        if "to" not in self.data.attributes.keys():
            raise AttributeError(
                "You need to provide the propriety `to` with a filepath on "
                "the element <file> to save the results to"
            )

    def __eq__(self, other: Any) -> bool:
        # TODO apply this logic to other __eq__ methods
        if type(self) == self.__class__ and type(other) == self.__class__:
            if self.content == other.content and self.to == other.to:
                return True
        return False

    def finish(self):
        print(f":: Saving {self.to}")
        ensure_dirs(Path(self.to).parent)
        with open(self.to, "w") as h:
            h.write(self.content)
