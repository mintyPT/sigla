import inspect


class NodeList(list):
    methods = [
        "__call__",
        "flatten",
        "uniq",
        "nonone",
        "get",
        "join",
    ]

    def __call__(self, sep="\n"):
        children = [c() for c in self]
        if sep:
            return sep.join(children)
        return children

    def flatten(self):
        ret = []
        for child in self:
            if not child:
                continue
            if hasattr(child, "flatten"):
                ret += child.flatten()
            elif isinstance(child, list):
                ret += child
            else:
                raise Exception(f"Case not accounted for: {type(child)}")
        return self.__class__(ret)

    def uniq(self):
        ret = self.__class__()
        for child in self:
            if child not in ret:
                ret.append(child)
        return ret

    def nonone(self):
        return self.__class__(filter(lambda e: e is not None, self))

    def get(self, name):
        return self.__class__(map(lambda e: getattr(e, name, None), self))

    def join(self, sep):
        return sep.join(self)

    @classmethod
    def get_node_list_methods(cls):
        methods_children = []
        for method in cls.methods:
            args = inspect.getfullargspec(getattr(NodeList, method)).args
            args = [a for a in args if a not in ["self"]]
            method = f".{method}" if method != "__call__" else ""
            methods_children.append(f"node.children{method}({','.join(args)})")
        return methods_children
