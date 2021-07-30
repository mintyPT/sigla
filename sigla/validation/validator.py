# TODO: Type validations
from typing import Any, Dict


class Validator:
    def __init__(self, validations) -> None:
        self.validations = validations

    def validate(self, data: Dict) -> Dict[str, Any]:
        values = {}
        for field, validations_for_field in self.validations.items():
            for validation in validations_for_field:
                validation(field, data.get(field))

            values[field] = data.get(field)

        return values


# TODO add example of validations to pass in
