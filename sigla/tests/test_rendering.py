from sigla.lib2.funcs import from_import_node_to_base_node
from sigla.lib2.importers.xml import load_xml
from sigla.tests.helpers import MemoryNodeTemplate

expected = '''
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
'''

definition = '''
<apifier-root>
    <apifier-block name="auth">
        <apifier-call name="me"/>
        <apifier-call name="login" method="POST"/>
        <apifier-call name="logout" method="POST"/>
    </apifier-block>
    <apifier-block name="users">
        <apifier-crud name="users" singular="user" urlprefix=""/>
        <apifier-block name="bookmarks">
            <apifier-crud name="bookmarks" singular="bookmark" urlprefix="/users/:user-id"/>
        </apifier-block>
    </apifier-block>
    <apifier-block name="bookmarks">
        <apifier-crud name="bookmarks" singular="bookmark" urlprefix=""/>
    </apifier-block>
</apifier-root>
'''


class TestRendering:
    def test_simple(self):
        node = MemoryNodeTemplate("b", {"name": "minty", "age": "33"})
        got = node.process()
        assert got == "minty-33"

    def test_simple_with_frontmatter(self):
        provided = """
        <person name="minty" age="33" />
        """
        got = from_import_node_to_base_node(
            load_xml(provided), TemplateClass=MemoryNodeTemplate
        ).process()

        assert got == "minty-sigla-33"

    def test_context_through_file(self):
        provided = """
        <echo name="minty" age="33" >
            <person />
        </echo>
        """
        got = from_import_node_to_base_node(
            load_xml(provided), TemplateClass=MemoryNodeTemplate
        ).process()

        assert got.content == "minty-sigla-33"

    def test_render_child(self):
        node = MemoryNodeTemplate("a", {})
        node.append(MemoryNodeTemplate("b", {"name": "minty", "age": "33"}))
        got = node.process()
        assert got == "-a-minty-33-a-"

        node.tag = "a2"
        got = node.process()
        assert got == "-a-minty-33-a-"

    def test_render_context2(self):
        provided = """
        <ta ra="one/">
            <tb name="ttbb" rb="two/">
                <tc name="three" />
            </tb>
        </ta>
        """
        got = from_import_node_to_base_node(
            load_xml(provided), TemplateClass=MemoryNodeTemplate
        ).process()
        assert got == "one/two/three"

    def test_fm_child(self):
        provided = """
        <first-level>
            <second-level>
                <third-level>
                </third-level>
            </second-level>
        </first-level>
        """
        got = from_import_node_to_base_node(
            load_xml(provided), TemplateClass=MemoryNodeTemplate
        ).process()
        assert got == "__one/two/three__"

    def test_big(self):
        got = from_import_node_to_base_node(
            load_xml(definition), TemplateClass=MemoryNodeTemplate
        ).process()
        assert got.replace(" ", "").replace("\n", "") == expected.replace(" ", "").replace("\n", "")
