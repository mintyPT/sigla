from textwrap import dedent

from sigla.template_loaders.template_loader import TemplateLoader


def _(template):
    return dedent(template)


class MemoryTemplateLoader(TemplateLoader):
    def write(self, content, tag, *, bundle=None):
        pass

    @property
    def templates(self):
        templates = {
            "person_v2": "My name is {{name}} and I'm {{age}} years old",
            "var": "{{ node.value | wrap }}",
            "ta": "{{ render(children) }}",
            "tb": "{{ render(children) }}",
            "tc": "{{ node.ra }}{{ node.rb }}{{ node.name }}",
            "nurse/persona": "This nurse's name is {{ node.name }}",
            "person_v4": self.person_v4(),
            "persons": self.persons(),
            "first_level": self.first_level(),
            "second_level": self.second_level(),
            "third_level": self.third_level(),
            "new_person": self.new_person(),
            "apifier_call": self.apifier_call(),
            "apifier_crud": self.apifier_crud(),
            "apifier_root": self.apifier_root(),
            "apifier_block": self.apifier_block(),
        }
        return {k: _(v).lstrip() for k, v in templates.items()}

    def load(self, tag, *, bundle=None):

        if bundle:
            tag = f"{bundle}/{tag}"

        if tag in self.templates:
            return _(self.templates[tag])

        raise Exception(f"Template `{tag}` not found")

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
