import math
import networkx as nx
from typing import Dict, List, Set, Tuple

from .var_alloc import Allocator, VarAllocContext
from .code_gen import Procedure


class TargetCode:

    code: List[Tuple[int, int]]
    input_primes: List[int]
    output_primes: List[int]

    def __init__(
        self,
        code: List[Tuple[int, int]],
        i_p: List[int],
        o_p: List[int]
    ) -> None:
        for n, d in code:
            if math.gcd(n, d) != 1:
                raise ValueError(
                    f'fractions in code not in simplest form: {n}/{d}'
                )
        
        self.code = code
        self.input_primes = i_p
        self.output_primes = o_p
        

class CodeGeneration:

    io_size: Tuple[int, int]
    procs: Dict[str, Procedure]

    def __init__(
            self,
            procs: List[Tuple[str, Procedure]],
            io_size: Tuple[int, int]
        ):
        self.procs = {k: v for k, v in procs}
        self.io_size = io_size

    def prime_allocation(self) -> TargetCode:
        g = nx.DiGraph()
        g.add_nodes_from(self.procs.keys())
        for s, p in self.procs.items():
            for used in p.proc_usage:
                g.add_edge(s, used)

        try:
            nx.cycles.find_cycle(g)
        except nx.exception.NetworkXNoCycle:
            pass
        else:
            raise RuntimeError('cycle detected in procedure invocation')
        
        nodes = nx.dag.topological_sort(g)
        sorted_procedures = [(n, self.procs[n]) for n in nodes]

        n_primes = sum(self.io_size)
        n_primes += sum(
            p.n_locals + 2 * len(p.code)
            for p in self.procs.values()
        )

        alloc = Allocator(n_primes)

        # IO allocation
        input_primes = alloc.allocate(self.io_size[0])
        i_map = {k: v for k, v in zip(range(self.io_size[0]), input_primes)}

        output_primes = alloc.allocate(self.io_size[1])
        o_map = {k: v for k, v in zip(range(self.io_size[1]), output_primes)}

        # procedure index allocation
        p_map = {}
        for s, p in sorted_procedures:
            index_primes = alloc.allocate(2 * len(p.code))
            p_map[s] = p.set_seg_indices(index_primes)

        ctx = VarAllocContext(p_map, i_map, o_map)

        # local variable allocation
        locals_map: Dict[str, Dict[int, int]] = {}
        for s, p in sorted_procedures:
            local_primes = alloc.allocate(p.n_locals)
            locals_map[s] = {k: v for k, v in enumerate(local_primes)}

        # code generation for each procedure
        target_code: List[Tuple[int, int]] = []
        for s, p in sorted_procedures:
            ctx.set_locals_map(locals_map[s])
            proc_code = p.code_gen(ctx)
            target_code.extend(proc_code)

        output = TargetCode(target_code, input_primes, output_primes)
        return output
