import networkx as nx
from typing import List, Set, Tuple

from .two_addrs import IRCode, ProcedureInfo, ProcedureIR, ParamType, LocalVar


def create_control_flow_graph(code: List[IRCode]) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_nodes_from(range(len(code)))

    info = ProcedureInfo({}, len(code))
    for idx, c in enumerate(code):
        succs = c.get_next_cfg(idx, info)
        graph.add_edges_from((c, s) for s in succs)
    
    return graph


def liveness(proc: ProcedureIR) -> List[Set[str]]:
    length = len(proc.code)
    live = [set() for _ in range(length)]
    cfg = create_control_flow_graph(proc.code)
    out_vars = {k for k, v in proc.params_type.items() if v == ParamType.OUT}

    for node, deg in cfg.out_degree():
        if deg == 0:
            live[node].update(out_vars)

    changed = True
    while changed:
        changed = False

        for lineno in range(length - 1, -1, -1):
            next_live_set = set.union(
                proc.code[i].get_live_locals()
                for i in cfg.successors(lineno)
            )

            unlive_vars = proc.code[lineno].get_unlive_locals()
            used_vars = proc.code[lineno].get_live_locals()

            live_vars = next_live_set.difference(unlive_vars).union(used_vars)
            if live_vars != live[lineno]:
                live[lineno] = live_vars
                changed = True

    return live
