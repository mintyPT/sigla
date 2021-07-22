import unittest

from sigla.actions import AddAction
from sigla.data.data import Data
from sigla.data.validation import RequiredValidation, required, validate_data


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
            validate_data(data, validations)
