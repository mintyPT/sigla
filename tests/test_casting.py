import unittest

from sigla.helpers.helpers import cast_property


class TestCastingProps(unittest.TestCase):
    def test_cast_int(self):
        self.assertEqual(cast_property("age-int", "23"), ("age", 23))

    def test_cast_float(self):
        self.assertEqual(
            cast_property("height-float", "1.87"), ("height", 1.87)
        )

    def test_cast_json(self):
        self.assertEqual(
            cast_property("data-json", '{"name": "mauro"}'),
            ("data", {"name": "mauro"}),
        )

    def test_cast_bool(self):
        adult_true = ("adult", True)
        adult_false = ("adult", False)

        self.assertEqual(cast_property("adult-bool", "true"), adult_true)
        self.assertEqual(cast_property("adult-bool", "True"), adult_true)
        self.assertEqual(cast_property("adult-bool", "1"), adult_true)
        self.assertEqual(cast_property("adult-bool", "TrUe"), adult_true)

        self.assertEqual(cast_property("adult-bool", "0"), adult_false)
        self.assertEqual(cast_property("adult-bool", "false"), adult_false)
        self.assertEqual(cast_property("adult-bool", "False"), adult_false)
        self.assertEqual(cast_property("adult-bool", "FalsE"), adult_false)
        self.assertEqual(
            cast_property("adult-bool", "anything-else"), adult_false
        )
