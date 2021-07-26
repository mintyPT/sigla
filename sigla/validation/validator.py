class Validator:
    def __init__(self, validations):
        self.validations = validations

    def validate(self, data: dict):
        values = {}
        for field, validations_for_field in self.validations.items():
            for validation in validations_for_field:
                validation(field, data.get(field))

            values[field] = data.get(field)

        return values

# TODO add example of validations to pass in
