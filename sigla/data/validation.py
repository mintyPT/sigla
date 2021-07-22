# TODO test this
# TODO convert this to class
from sigla.data.helpers import get_default_value_for_attribute


def validate_data(data, validations):
    values = {}
    for field, validations_for_field in validations.items():
        values[field] = get_default_value_for_attribute(data, field)

        for validation in validations_for_field:
            validation(field, values[field])

    return values


class RequiredValidation(Exception):
    pass


def required():
    def validate(field, value):
        if value is None:
            raise RequiredValidation(f"{field} is required")

    return validate
