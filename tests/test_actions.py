import unittest

from sigla.actions.actions import AddAction
from sigla.data.data import Data
from sigla.validation.validator import Validator
from sigla.validation.validation_required import RequiredValidation, required


class TestAction(unittest.TestCase):
    def test_buffer_action(self):
        pass

    def test_add_action(self):
        pass

    def test_add_action_path_required(self):
        with self.assertRaises(RequiredValidation):
            data = Data("person")
            AddAction(data, "")

    def test_modify_action(self):
        pass

    def test_append_action(self):
        pass

    def test_data_validator(self):
        validations = {"path": [required()]}
        data = Data("person")

        with self.assertRaises(RequiredValidation):
            validator = Validator(validations)
            validator.validate(data)
