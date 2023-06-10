from typing import Dict, List, Tuple

from .var_alloc import Allocator, CodeGenContext
from .code_gen import Procedure


class TargetProgram:

    io_size: Tuple[int, int]
    procs: Dict[str, Procedure]

    def __init__(
            self,
            procs: List[Tuple[str, Procedure]],
            io_size: Tuple[int, int]
        ):
        self.procs = {k: v for k, v in procs}
        self.io_size = io_size

    def prime_allocation(self) -> None:
        # TODO: togological sort on procedures

        n_primes = sum(self.io_size)
        n_primes += sum(
            p.locals_size() + p.index_size()
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
        for s, p in self.procs.items():
            index_primes = alloc.allocate(p.index_size())
            p_map[s] = p.set_seg_indices(index_primes)

        ctx = CodeGenContext(p_map, i_map, o_map)

        # local variable allocation
        
