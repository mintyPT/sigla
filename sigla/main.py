from sigla.node_loaders import DataToNodeLoader, XMLToNodeLoader
from sigla.nodes.abstract_node import AbstractNode


def process(kind, content, *, factory=None):
    node = load_node(kind, content, factory=factory)
    node.process()
    node.finish()


def load_node(kind, content, *, factory=None) -> AbstractNode:
    if kind == "data":
        return DataToNodeLoader(content, factory).load()
    elif kind == "xml":
        return XMLToNodeLoader(content, factory).load()
    else:
        raise NotImplementedError(f"No loader implemented for {kind}")
