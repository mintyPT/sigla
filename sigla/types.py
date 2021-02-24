from typing import Union
from sigla.core.nodes.NodeEcho import NodeEcho
from sigla.core.nodes.NodeFile import NodeFile
from sigla.core.nodes.NodeRoot import NodeRoot
from sigla.core.nodes.NodeTemplate import NodeTemplate

NodeType = Union[NodeRoot, NodeFile, NodeEcho, NodeTemplate]
