class RequiredValidation(Exception):
    pass


def required():
    def validate(field, value):
        if not value:
            raise RequiredValidation(f"{field} is required")

    return validate
