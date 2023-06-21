import networkx as nx
from typing import Dict


# TODO: implement a Riggs' allocator (as TAC isn't a chordal graph)
# braindead implementation of reg alloc cuz i wanna get this finished before
# dmp end qwq
def reg_alloc(g: nx.DiGraph) -> Dict[str, int]:
    nodes = list(g.nodes())
    return {n: id for id, n in enumerate(nodes)}
