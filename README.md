**Note:** This is a WIP for the v1.0 so stuff might be broken but not for long

# Sigla...

Is a code generator dressed as a cli. It is intended to help you generate code (or any text really) the easiest why possible. The core idea for the code generator came from the book "Code Generation in Action" by Jack Herrington, but with extra stuff built into it.

There are two thinks to understand about this cli:

1. This cli is mean to allow you to generate your code, make some changes and re-generate the code. The improvement and updating of the templates is meant to me made iteratively. This goes specially well with object oriented languages where you can manually write classes that extend generated ones. You can always just generate the code once, but you are throwing away so much potential.
2. Despite being coded in python, the generator is meant and capable to generate code for any language or just simple text. As of this day, I've used it to generate a complete django rest framework api (complete with simple views, serializers, fixtures, seeds and test) and also, a frontend built in react.

To use it, you'll need to have some basic knowledge of python, xml, jinja and ideally frontmatter.  


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sigla.

```bash
pip install sigla
```


## Usage

### Basic workflow

The use of sigla is rather simple. Start by initializing sigma using the command line

```bash
sigla init
```

This will create a directory named `.sigma` were it will store data (definitions, templates, filters, configurations and snapshots) related to your code generation. Next, create a new definition (xml file) to old the data to generate you code:

```bash
poetry run sigla nd person
``` 

This will generate a new definition file `.sigla/definitions/person.xml`. Fill that definition with something along the lines of:

```xml
<file to="people.txt">
    <person name="james" age="33" />
</file>
```    

Exempting `file`, `root` and `echo`, you can use any (xml valid) name for the tag inside the xml file. For the attributes, you can use any valid xml attribute name. Now to the good stuff: once your data is filled and properly saved, run the generator:

```bash
poetry run sigla rd person
``` 

Since this is the first time running the code generator and since you have no templates: sigla will create them for you. Take a look at the newly created template `.sigla/template/peson.jinja2` and update its content to match the following:

```my name is {{ name }} and I'm {{ age }} years old```
    
    
If you rerun the generator and look into `people.txt`, you should see the result: 


```my name is james and I'm 33 years old```

You just completed your first generator.


### Lists

We've seen how to make a simple code generator by considering only one person. What if you wish to generate the same but for your family? In that case, the data becomes:

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

Run the generator again. It should create a new template `family.ninja2` that you should update with:

```
My family presentations:

{{ render(children) }}
```

or
 
```
My family presentations:
{% for child in children %}
    {{ render(child) }}
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

Since you know about `<file/>` and `<root/>` it is time to mention that you do have to generate a single file from a definition like it was showed previously. So, each definition file can be responsible for the generation of multiple files. To do it, simple add more `<file/>` wrapped into a `<root/>`. Example:

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

```my name is {{ name }} {{ family_name }} and I'm {{ age }} years old```

To generate this:

```my name is james hopkins and I'm 33 years old```



### Frontmatter

Todo...

### Custom filters file

Todo...

### Vars available inside templates

Todo...

### Access to children meta data (frontmatter)

Todo...





## Contributing

Like most of my projects, this own grew to scratch my own itch. It is so useful that it should be shared. Since this is the first time that I'm publishing something hopping that others might find it useful, I'll do my best to write some documentation and tests (this is the first time I'm doing so).

Pull requests are more than welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

