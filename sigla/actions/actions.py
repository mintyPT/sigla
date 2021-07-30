from abc import ABC, abstractmethod
from pathlib import Path
from textwrap import dedent

from sigla.data.data import Data
from sigla.validation.validation_required import required
from sigla.validation.validator import Validator


class Action(ABC):
    validations = {}

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def __init__(self, data: Data, result: str):
        self.data: Data = data
        self.result = result
        validator = Validator(self.validations)
        # TODO how to say that this is valid?
        self.params = validator.validate(self.data)

    @abstractmethod
    def execute(self) -> None:
        pass


class BufferAction(Action):
    name = "buffer"

    def execute(self) -> None:
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

    def execute(self) -> None:
        path = Path(self.params["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.result)


class ModifyAction(Action):
    name = "modify"

    validations = {
        "path": [required()],
        "pattern": [required()],
    }

    def execute(self) -> None:
        # TODO finish this
        raise NotImplementedError


class AppendAction(Action):
    name = "append"

    validations = {
        "path": [required()],
        # TODO implement pattern
        # "pattern": [required()],
    }

    def execute(self) -> None:
        with Path(self.params["path"]).open("a") as f:
            f.write(self.result)


actions = {
    BufferAction.name: BufferAction,
    AddAction.name: AddAction,
    ModifyAction.name: ModifyAction,
    AppendAction.name: AppendAction,
}
