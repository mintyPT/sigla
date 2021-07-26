from textwrap import dedent

from sigla.template_loaders.template_loaders import TemplateLoader


def _(template):
    return dedent(template)


class MemoryTemplateLoader(TemplateLoader):
    def write(self, content, path):
        pass

    @property
    def templates(self):
        templates = {
            "person_v2.jinja2": "My name is {{name}} and I'm {{age}} years old",
            "var.jinja2": "{{ node.value | wrap }}",
            "ta.jinja2": "{{ render(children) }}",
            "tb.jinja2": "{{ render(children) }}",
            "tc.jinja2": "{{ node.ra }}{{ node.rb }}{{ node.name }}",
            "nurse/persona.jinja2": "This nurse's name is {{ node.name }}",
            "person_v4.jinja2": self.person_v4(),
            "persons.jinja2": self.persons(),
            "first_level.jinja2": self.first_level(),
            "second_level.jinja2": self.second_level(),
            "third_level.jinja2": self.third_level(),
            "new_person.jinja2": self.new_person(),
            "apifier_call.jinja2": self.apifier_call(),
            "apifier_crud.jinja2": self.apifier_crud(),
            "apifier_root.jinja2": self.apifier_root(),
            "apifier_block.jinja2": self.apifier_block(),
        }
        return {k: _(v).lstrip() for k, v in templates.items()}

    def load(self, path):
        if path in self.templates:
            return _(self.templates[path])

        raise Exception(f"Template `{path}` not found")

    @staticmethod
    def apifier_block():
        return """
            ---
            name:  "sigla"
            ---
            "{{ node.name }}": { {% for child in node.children %}
                {{ render(child) | indent(8) }},
            {%- endfor %}
            }
            """

    @staticmethod
    def apifier_root():
        return """
            ---
            name:  "sigla"
            ---
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
            {% for child in node.children %}
                {{ render(child) | indent(8) }},
            {% endfor %}
            }
            """

    @staticmethod
    def apifier_crud():
        return """
            "list": call_wrapper("{{ node.urlprefix }}/{{ node.name }}", method="GET"),
            "create": call_wrapper("{{ node.urlprefix }}/{{ node.name }}", method="POST"),
            "read": call_wrapper("{{ node.urlprefix }}/{{ node.name }}/:id", method="GET"),
            "update": call_wrapper("{{ node.urlprefix }}/{{ node.name }}/:id", method="PUT"),
            "update_p": call_wrapper("{{ node.urlprefix }}/{{ node.name }}/:id", method="PUT"),
            "delete": call_wrapper("{{ node.urlprefix }}/{{ node.name }}/:id", method="DELETE")
            """

    @staticmethod
    def apifier_call():
        return """
            "{{ node.name }}": call_wrapper("/{{ node.name }}", {{ _(node.attributes).without("name").as_kwargs().val() }})
            """

    @staticmethod
    def new_person():
        return """
            ---
            second_name: "sigla"
            ---
            {{- node.name }}-{{ node.second_name }}-{{ node.age }}
            """

    @staticmethod
    def third_level():
        return """
            ---
            lower: "three"
            ---
            """

    @staticmethod
    def second_level():
        return """
            ---
            me: "two"
            ---
            {% set lower = _(node.children).flatten().get('lower').nonone().join(',').val() -%}
            __{{ node.upper }}/{{ node.me }}/{{ lower }}__
            """

    @staticmethod
    def first_level():
        return """
            ---
            upper: "one"
            ---
            {{ render(children) }}
            """

    @staticmethod
    def persons():
        return """
            Persons:
            {{ render(children) }}
            """

    @staticmethod
    def person_v4():
        return """
            ---
            name: "{{ name }} {{ family }}"
            ---
            My name is {{name}} and I\'m {{age}} years old
            """
