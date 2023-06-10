from typing import Dict, List, Tuple

from .var_alloc import Allocator
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
        
        n_primes = self.io_size[0] + self.io_size[1]
        n_primes += sum(p.allocation_size() for p in self.procs.values())
        alloc = Allocator(n_primes)
