import unittest
from sigla.utils.type_casters import cast_property


class TestCastingProps(unittest.TestCase):
    def test_tag_props_conversion(self):
        tests = [
            # int
            [("age-int", "23"), ("age", 23)],
            # bool
            [("adult-bool", "true"), ("adult", True)],
            [("adult-bool", "True"), ("adult", True)],
            [("adult-bool", "1"), ("adult", True)],
            [("adult-bool", "TrUe"), ("adult", True)],
            # float
            [("height-float", "1.87"), ("height", 1.87)],
            # json
            [
                ("data-json", '{"name": "mauro"}'),
                ("data", {"name": "mauro"}),
            ],
        ]

        for args, results in tests:
            self.assertEqual(cast_property(*args), results)
