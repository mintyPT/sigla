import unittest
from textwrap import dedent

from sigla.data.data_loaders.xml_to_data import convert_xml_string_to_data
from sigla.engines.engines import SiglaEngine
from tests.helpers.memory_template_loader import MemoryTemplateLoader

template_loader = MemoryTemplateLoader()

provided = """
    <buffer>
        <apifier_root>
            <apifier_block name="auth">
                <apifier_call name="me"/>
                <apifier_call name="login" method="POST"/>
                <apifier_call name="logout" method="POST"/>
            </apifier_block>
            <apifier_block name="users">
                <apifier_crud name="users" singular="user" urlprefix=""/>
                <apifier_block name="bookmarks">
                    <apifier_crud name="bookmarks" singular="bookmark" urlprefix="/users/:user-id"/>
                </apifier_block>
            </apifier_block>
            <apifier_block name="bookmarks">
                <apifier_crud name="bookmarks" singular="bookmark" urlprefix=""/>
            </apifier_block>
        </apifier_root>
    </buffer>
"""  # noqa
expected = dedent(
    """
    def call_wrapper(url: str, method: str = "GET"):
        def call(query, body, params):
            print('call api')
            print('- url:', url)
            print('- method:', method)
            print('- query:', query)
            print('- body:', body)
            print('- params:', params)
        return call


    apifier = {


            "sigla": {
                "me": call_wrapper("/me", ),
                "login": call_wrapper("/login", method="POST"),
                "logout": call_wrapper("/logout", method="POST"),
            },


            "sigla": {
                "list": call_wrapper("/users", method="GET"),
                    "create": call_wrapper("/users", method="POST"),
                    "read": call_wrapper("/users/:id", method="GET"),
                    "update": call_wrapper("/users/:id", method="PUT"),
                    "update_p": call_wrapper("/users/:id", method="PUT"),
                    "delete": call_wrapper("/users/:id", method="DELETE"),

                    "sigla": {
                        "list": call_wrapper("/users/:user-id/bookmarks", method="GET"),
                            "create": call_wrapper("/users/:user-id/bookmarks", method="POST"),
                            "read": call_wrapper("/users/:user-id/bookmarks/:id", method="GET"),
                            "update": call_wrapper("/users/:user-id/bookmarks/:id", method="PUT"),
                            "update_p": call_wrapper("/users/:user-id/bookmarks/:id", method="PUT"),
                            "delete": call_wrapper("/users/:user-id/bookmarks/:id", method="DELETE"),
                    },
            },


            "sigla": {
                "list": call_wrapper("/bookmarks", method="GET"),
                    "create": call_wrapper("/bookmarks", method="POST"),
                    "read": call_wrapper("/bookmarks/:id", method="GET"),
                    "update": call_wrapper("/bookmarks/:id", method="PUT"),
                    "update_p": call_wrapper("/bookmarks/:id", method="PUT"),
                    "delete": call_wrapper("/bookmarks/:id", method="DELETE"),
            },

    }
    """
)  # noqa: E501


class TestRendering(unittest.TestCase):
    def test_simple(self):
        provided = (
            '<buffer><person_v2 name="mauro" age="34"></person_v2></buffer>'
        )
        expected = "My name is mauro and I'm 34 years old"

        data = convert_xml_string_to_data(provided)
        engine = SiglaEngine.render_from_data(data, template_loader)
        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_double(self):
        provided = """
            <buffer>
                <person_v2 name="mauro" age="34"></person_v2>
                <person_v2 name="mauro" age="34"></person_v2>
            </buffer>
        """

        expected = "My name is mauro and I'm 34 years old\nMy name is mauro and I'm 34 years old"

        engine = SiglaEngine.render_from_xml(provided, template_loader)

        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_indented(self):
        provided = """
            <buffer>
                <persons>
                    <person_v2 name="mauro" age="34"></person_v2>
                    <person_v2 name="mauro" age="34"></person_v2>
                </persons>
            </buffer>
        """
        expected = dedent(
            """
            Persons:
            My name is mauro and I'm 34 years old
            My name is mauro and I'm 34 years old
        """
        ).lstrip()

        engine = SiglaEngine.render_from_xml(provided, template_loader)
        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_attributes_from_parent(self):
        provided = """<buffer name="minty" age="33"><person_v2 /></buffer>"""
        expected = "My name is minty and I'm 33 years old"

        engine = SiglaEngine.render_from_xml(provided, template_loader)
        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_filter_inject(self):
        provided = "<buffer><var value='a'/></buffer>"
        expected = "[a]"
        filters = {"wrap": lambda e: f"[{e}]"}
        engine = SiglaEngine.render_from_xml(
            provided, template_loader, filters=filters
        )
        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_fm_child(self):
        provided = """
            <buffer>
                <first_level>
                    <second_level>
                        <third_level>
                        </third_level>
                    </second_level>
                </first_level>
            </buffer>
        """
        expected = "__one/two/three__\n\n"
        engine = SiglaEngine.render_from_xml(provided, template_loader)
        self.assertEqual(expected, engine.artifacts[-1].result)

    # TODO
    def test_simple_with_frontmatter(self):
        provided = """
        <buffer>
            <new_person name="minty" age="33" />
        </buffer>
        """
        expected = "minty-sigla-33\n"
        engine = SiglaEngine.render_from_xml(provided, template_loader)
        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_render_context2(self):
        provided = """
        <buffer>
            <ta ra="one/">
                <tb name="ttbb" rb="two/">
                    <tc name="three" />
                </tb>
            </ta>
        </buffer>
        """
        expected = "one/two/three"

        engine = SiglaEngine.render_from_xml(provided, template_loader)
        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_bundling(self):
        provided = '<buffer><persona bundle="nurse" name="Jeanne"/></buffer>'
        expected = "This nurse's name is Jeanne"
        engine = SiglaEngine.render_from_xml(provided, template_loader)
        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_big_one(self):
        engine = SiglaEngine.render_from_xml(provided, template_loader)
        self.assertEqual(
            expected.replace(" ", "").replace("\n", ""),
            engine.artifacts[-1].result.replace(" ", "").replace("\n", ""),
        )

    def test_frontmatter_rendering(self):
        provided = '<buffer name="minty" age="33"><person_v4 family="santos" /></buffer>'
        expected = "My name is minty santos and I'm 33 years old\n"

        engine = SiglaEngine.render_from_xml(provided, template_loader)
        self.assertEqual(expected, engine.artifacts[-1].result)

    def test_2(self):
        provided = """
            <buffer name="minty1" age="1">
                <buffer name="minty2" age="2">
                    <buffer name="minty3" age="3">
                        <person_v4 family="santos" />
                    </buffer>
                </buffer>
            </buffer>
        """
        expected = "My name is minty3 santos and I'm 3 years old\n"

        engine = SiglaEngine.render_from_xml(provided, template_loader)
        got = engine.artifacts[-1].result

        self.assertEqual(expected, got)


# TODO
# <models>
#   <model name="User">
#     ...
#   </model>
# </models>
# <forms>
#   <user_form model="User"
#       /or/ model-query="models model[name='User']" /or/ $model="User">
#     ...
#   </user_form>
# </forms>


# TODO test raise template not found
# TODO create templates automatically
# TODO test/finish script prop run and merge attributes
