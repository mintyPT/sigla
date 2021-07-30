from typing import Any, Callable


class RequiredValidation(Exception):
    pass


def required() -> Callable[[str, Any], None]:
    def validate(field: str, value: Any) -> None:
        if not value:
            raise RequiredValidation(f"{field} is required")

    return validate
