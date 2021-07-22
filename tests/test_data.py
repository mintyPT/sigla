import unittest

from sigla.data.data import Data


class TestData(unittest.TestCase):
    def test_simple(self):
        data = Data("model")
        self.assertEqual(data.tag, "model")
        self.assertEqual(data.attributes, {})

    def test_with_attribute(self):
        data = Data("model", name="User")
        self.assertEqual(data.tag, "model")
        self.assertEqual(data.attributes, {"name": "User"})
        self.assertEqual(data.name, "User")

    def test_iterate_children(self):
        names = ["User", "Pet"]

        data = Data(
            "models",
            children=[
                Data("model", name=names[0]),
                Data("model", name=names[1]),
            ],
        )

        for i, child in enumerate(data):
            self.assertEqual(child.name, names[i])

    def test_inherit_parent_attributes(self):
        data = Data(
            "models",
            namespace="secret",
            namespace2="not-secret",
            children=[
                Data(
                    "model",
                    name="User",
                    namespace2="secret",
                ),
                Data(
                    "model",
                    name="Pet",
                    namespace2="secret",
                ),
            ],
        )

        for i, child in enumerate(data):
            self.assertEqual(child.namespace, "secret")
            self.assertEqual(child.namespace2, "secret")

    def test_equal(self):
        data = Data(
            "models",
            namespace="secret",
            namespace2="not-secret",
            children=[
                Data(
                    "model",
                    name="User",
                    namespace2="secret",
                ),
                Data(
                    "model",
                    name="Pet",
                    namespace2="secret",
                ),
            ],
        )
        data2 = Data(
            "models",
            namespace="secret",
            namespace2="not-secret",
            children=[
                Data(
                    "model",
                    name="User",
                    namespace2="secret",
                ),
                Data(
                    "model",
                    name="Pet",
                    namespace2="secret",
                ),
            ],
        )

        self.assertEqual(data, data2)
