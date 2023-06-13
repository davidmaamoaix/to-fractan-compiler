import networkx as nx
from typing import List, Set, Tuple

from .two_addrs import IRCode, ControlFlowInfo


class CFG:

    graph: nx.DiGraph

    def __init__(self, code: List[IRCode]) -> None:
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(range(len(code)))

        info = ControlFlowInfo({}, len(code))
        for idx, c in enumerate(code):
            succs = c.get_next_cfg(idx, info)
            self.graph.add_edges_from((c, s) for s in succs)


class LiveContext:
    
    length: int
    live_in: List[Set[str]]
    live_out: List[Set[str]]

    def __init__(self, length: int) -> None:
        self.length = length
        self.live_in = [set() for _ in range(self.length)]
        self.live_out = [set() for _ in range(self.length)]