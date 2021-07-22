from abc import ABC, abstractmethod
from pathlib import Path
from textwrap import dedent

from sigla.data.data import Data
from sigla.data.validation import required, validate_data


class Action(ABC):
    validations = {}

    @property
    @abstractmethod
    def name(self):
        pass

    def __init__(self, data: Data, result: str):
        self.data: Data = data
        self.result = result
        self.params = validate_data(self.data, self.validations)

    @abstractmethod
    def execute(self):
        pass


class BufferAction(Action):
    name = "buffer"

    def execute(self):
        separator = "=" * 40
        print(
            dedent(
                f"""
            {separator}
            Result for buffer:
            ```
            %s
            ```

            Representation of buffer's data:
            ```
            %s
            ```
            {separator}
            """
            )
            % (self.result, self.data.render())
        )


class AddAction(Action):
    name = "add"
    validations = {"path": [required()], "skipIfExists": []}  # default: false

    def execute(self):
        Path(self.params["path"]).write_text(self.result)


class ModifyAction(Action):
    name = "modify"

    validations = {
        "path": [required()],
        "pattern": [required()],
    }

    def execute(self):
        # TODO finish this
        raise NotImplementedError


class AppendAction(Action):
    name = "append"

    validations = {
        "path": [required()],
        # TODO implement pattern
        # "pattern": [required()],
    }

    def execute(self):
        with Path(self.params["path"]).open("a") as f:
            f.write(self.result)


actions = {
    BufferAction.name: BufferAction,
    AddAction.name: AddAction,
    ModifyAction.name: ModifyAction,
    AppendAction.name: AppendAction,
}
