from xml.etree import ElementTree as ET


class Node(object):
    attributes = {}
    meta = {}
    children = []

    def __init__(self, children=None, attributes=None, meta=None):
        if children is None:
            children = []
        if attributes is None:
            attributes = {}
        if meta is None:
            meta = {}

        self.attributes = attributes
        self.meta = meta
        self.children = children

    @classmethod
    def from_xml(cls, node: ET.Element):
        attributes = {}
        children = []
        for k, v in node.attrib.items():

            if k.endswith('-int'):
                attributes[k.replace('-int', '')] = int(v)
            else:
                attributes[k] = v
        for child in node:
            children.append(cls.from_xml(child))

        meta = {
            'tag': node.tag.split('-')[-1],
            'otag': node.tag  # otag => original tag
        }

        return cls(children=children, attributes=attributes, meta=meta)

    def prettyprint(self, depth=0):
        sep = ' ' * depth * 4
        if len(self.children) > 0:
            child = "\n" + \
                    "\n".join(map(lambda x: x.prettyprint(depth=depth + 1), self.children)) + \
                    f"\n{sep}"
        else:
            child = ''
        return f"""{sep}<{self.tag} {repr(self.attributes)}>{child}</{self.tag}>"""

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError as e:
            if name in self.attributes.keys():
                return self.attributes[name]
            elif name in self.meta.keys():
                return self.meta[name]
            else:
                raise e

    def __iter__(self):
        return iter(self.children)
