import unittest

from sigla import load_node
from tests.helpers.AutoNodeTemplate import AutoNodeTemplate
from .helpers.node_factory_for_testing import node_factory_for_testing

expected = """
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
"""  # noqa

definition = """
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
"""  # noqa


class TestRendering(unittest.TestCase):
    def test_simple(self):
        node = AutoNodeTemplate("b", {"name": "minty", "age": "33"})
        got = node.process()
        self.assertEqual(got, "minty-33")

    def test_simple_with_frontmatter(self):
        provided = """
        <person name="minty" age="33" />
        """
        got = load_node(
            "xml_string", provided, factory=node_factory_for_testing
        )()

        self.assertEqual(got, "minty-sigla-33")

    def test_context_through_file(self):
        provided = """
        <echo name="minty" age="33" >
            <person />
        </echo>
        """
        got = load_node(
            "xml_string", provided, factory=node_factory_for_testing
        )
        self.assertEqual(got.process().content, "minty-sigla-33")

    def test_filters(self):
        provided = "<var value='a'/>"
        got = load_node(
            "xml_string", provided, factory=node_factory_for_testing
        )
        self.assertEqual(got.process(), "[a]")

    def test_render_child(self):
        node = AutoNodeTemplate("a", {})
        node.append(AutoNodeTemplate("b", {"name": "minty", "age": "33"}))
        got = node.process()
        self.assertEqual(got, "-a-minty-33-a-")

        node.data.tag = "a2"
        got = node.process()
        self.assertEqual(got, "-a-minty-33-a-")

    def test_render_context2(self):
        provided = """
        <ta ra="one/">
            <tb name="ttbb" rb="two/">
                <tc name="three" />
            </tb>
        </ta>
        """
        got = load_node(
            "xml_string", provided, factory=node_factory_for_testing
        )()
        self.assertEqual(got, "one/two/three")

    def test_fm_child(self):
        provided = """
        <first_level>
            <second_level>
                <third_level>
                </third_level>
            </second_level>
        </first_level>
        """
        got = load_node(
            "xml_string", provided, factory=node_factory_for_testing
        )
        self.assertEqual(got.process(), "__one/two/three__")

    def test_big_one(self):
        self.maxDiff = None
        got = load_node(
            "xml_string", definition, factory=node_factory_for_testing
        ).process()

        self.assertEqual(
            got.replace(" ", "").replace("\n", ""),
            expected.replace(" ", "").replace("\n", ""),
        )

    def test_bundling(self):
        provided = """
        <persona bundle="nurse" name="Jeanne"/>
        """
        got = load_node(
            "xml_string", provided, factory=node_factory_for_testing
        )
        self.assertEqual(got.process(), "This nurse's name is Jeanne")
