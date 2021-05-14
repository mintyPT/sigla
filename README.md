**Note:** This is a WIP for the v1.0 so stuff might be broken but not for long

# Sigla

## Tasks 

- pass prop as array of x. ex names-array-string="[...]"
- ```<data></data>```
- ```<data-proxy></data-proxy>```
- ```<Partial>``` to inject into existing files

## Introduction

Sigla is a code generator.  Some important points about it: 

- It's is meant to be used as a cli (mostly);
- I will allow you to re-generate the templates whenever you need; Either because the data changed or the templates;
- It is intended to help you generate code or simple text in the easiest and most forward way possible. For this reasons we added an init command and the automatic creation of missing templates;
- The core idea for the code generator came from the book ["Code Generation in Action" by Jack Herrington](https://www.manning.com/books/code-generation-in-action), but with some extra magic built into it like frontmatter and a way to know the properties both parents and childrens of a node (more on this later).


## Requirements (knowledge)

There are two things you need to understand about sigla:

1. It has a clear workflow: 
    1. Create or modify the definition file for a generator (this is a xml file);
    2. Create or modify a template (this is a jinja file). You can add/modify frontmatter written in yaml;
    3. Feed the definition file into the generator;
    4. Repeat 1-3 as needed.
    
    The improvement of the templates and definition files are meant to be iterative, allowing you to re-generate the code any time you want. This pairs specially well with object oriented languages where you can generate some base classes and then extend those manually, overriding stuff as necessary. You can always just generate the code once, but you are throwing away so much potential. For example, we could generated a class like this in python
    
    ```python 
    class PersonGenerated(object):
        def __init__(self, first_name, last_name):
            self.first_name = first_name
            self.last_name = last_name 
    ```
   
   and then extend it like so 

    ```python 
    class Person(PersonGenerated):
        @property
        def full_name(self):
            return f"{self.first_name} {self.last_name}" 
    ```
   
   Obviously this is a trivial example, but I believe it illustrates the point on what to generate and where to go from there to get the maximum value.
      
 

2. Despite being coded in python, the generator is well capable of generating code for any language or project. As of this day, I've used it to generate a django rest framework api (includes views, serializers, fixtures, seeds and tests), a frontend built with react, some text (conversion of data to text).

## TODO
- definitions
- templates
- filters
- configurations
- snapshots
- special attributes for node and node.children


## Installation

Use a package manager to install sigla.

```bash
pip install sigla

poetry add sigla
```

## Requirements

Besides installing sigla, you'll need to have some basic knowledge of python, xml, jinja and ideally frontmatter to take full advantage of sigla.

## Usage

### Basic workflow

The use of sigla is rather simple. Start by initializing the necessary folder structure for sigla using the command line

```bash
sigla init
```

This will create a directory named `.sigla` to store the data related to your code generation. Next, create a new definition. This holds the config and structure for the code generation.

```bash
poetry run sigla new person
``` 
The new file can be located here: `.sigla/definitions/person.xml`. With definition files, you can do pretty much anything, as long as it's valid xml. All the data in this fill will later be present inside the templates.

Fill the definition with this:

```xml
<file to="people.txt">
    <person name="james" age="33" />
</file>
```    

This tells sigla to generate a new file called `person.txt`, where the content will come from the template `.sigla/templates/person.jinja2`. The person template will receive 2 variables called `name` and `age` that will be accessible through the `node` like this `node.name` and `node.age`. 

Exempting `file`, `root` and `echo`, which have special meaning, you can use any (valid xml) name for the tags inside the xml file and they'll have a matching template inside `.sigla/templates`. For the attributes, you can use any valid xml attribute name. 

Once your definition is filled and saved, run the generator:

```bash
poetry run sigla rd person
``` 

Since this is the first time running the code generator and you have no templates, sigla will create them for you. Take a look at the newly created template `.sigla/template/person.jinja2`. You can update its content with the following:

```my name is {{ node.name }} and I'm {{ node.age }} years old```
    
    
If you rerun the generator and look at the file `people.txt`, you should see the following result: 


```my name is james and I'm 33 years old```

You just completed your first generator and your first iteration. Now if you go back and change the name or the template, you can re-run the code generation to refresh the resulting code.


### Lists

We've seen how to make a simple code generator by considering only one person. What if you wish to generate the same but for your whole family? In that case, the data becomes:

```xml
<file to="people.txt">
    <family>
        <person name="james" age="33" />
        <person name="marie" age="29" />
        <person name="luke" age="45" />
        <person name="angela" age="50" />
    </family>
</file>
```    

Notice that this is the first time you encounter nesting. The only thing to know is that you can nest up to infinity and when writing the templates, the nested children will be available through `node.children`.

RunCommand the generator again to generated the new template: `family.ninja2`. You can update it like this:

```
My family presentations:

{{ node.children() }}
```

or 
 
```
My family presentations:
{% for child in node.children %}
    {{ child() }}
{% endfor %}
```

If you regenerate the code now, the result inside `people.txt` should be:

```
My family presentations:

my name is james and I'm 33 years old
my name is marie and I'm 29 years old
my name is luke and I'm 45 years old
my name is angela and I'm 50 years old
```

## Good to know

### Special tags

It was mentioned earlier that besides some special tags, you could use any tag inside the definition file. Here is the list of the special tags along with a small explanation of their behaviour:

- `<file to="{{ path }}">...</file>` will take the content of his children and save it to the filepath;
- `<echo>...</echo>` will print the content of his children once the generation is done;
- `<root>...</root>` does nothing. It's only a wrapper when you want to write multiple file exports but can't simply place them at the root of the xml file.


### Multiple outputs

Since you know about `<file/>` and `<root/>` it is a good time to mention that a valide xml file should have a single root node. That is why `<root/>` exists. If you want to generate more than one file from a single definition, simply wrapp all the `<file/>` with `<root/>`, like so:

```xml
<root>
    <file to="people.txt">
        <person name="james" age="33" />
    </file>
    <file to="pets.txt">
        <pet name="max" age="3" />
    </file> 
</root>
```    

After the generation, this will create 2 files: `people.txt` & `pets.txt`. 


### Context inheritance

It is important to note that the attributes from the parents are passed automatically to the children. If your data is:

```xml
<family familiy_name="hopkins">
    <person name="james" age="33" />
</family>
```    

Then, `family_name` will be available inside `person.jinja2` and as such, you can do this:

```my name is {{ node.name }} {{ node.family_name }} and I'm {{ node.age }} years old```

To generate this:

```my name is james hopkins and I'm 33 years old```



### Frontmatter

Todo...

### Custom filters file

Todo...

### Vars available inside templates

Todo...

### Access to children meta data (frontmatter)

We've seen you can render children either doing node.children() or iterating over node.children and rendering each child with child(). This important thing to notice is that a child is a node just like the base node we use on our templates. This mean you have access to its attributes, children and so on.

### Properties type conversion

Passing only string as the value of properties is slightly constraining. As such, there is a way to cast into other types of variables:

```xml
    <something 
        name='a' 
        age-int='33' 
        price-float='1.2' 
        data-json='{\"v1\": 1}' 
    />
```
Notice the `-int`, `-float` and `-json`.

The previous example will result into the following variables:
```json
{
    "name": "a",
    "age": 33,
    "price": 1.2,
    "data": {"v1": 1}
}
```

## Contributing

Like most of my projects, this one grew to scratch my own itch. It is so useful that it should be shared. Since this is the first time that I'm publishing something hoping that others might find it useful, I'll do my best to write some documentation and tests (this is the first time I'm doing so).

Pull requests are more than welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Poetry

If you wish to "locally" install this into another project, you can do it like so

```
sigla = { path = "../sigla/", develop = true }
```