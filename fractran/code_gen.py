import enum
from typing import Dict, List, Set, Tuple, Union

from .var_alloc import AllocVar, Allocator


FracCode = List[Tuple[List[AllocVar], List[AllocVar]]]


class ParamType(enum):
    IN = 0
    OUT = 1


class CodeSegment:
    
    # on initialization
    code: FracCode

    # after prime allocation
    index: Tuple[int, int]

    def __init__(self, code: FracCode):
        self.code = code

    def assign_index(self, alloc: Allocator) -> None:
        self.index = tuple(alloc.allocate(2))


class Procedure:

    # on initialization
    name: str
    locals_count: int # including the number of parameters
    params_type: List[ParamType]
    code: List[CodeSegment]
    proc_usage: Set[str]

    # after prime allocation
    locals_map: Dict[int, int]

    def __init__(
        self,
        name: str,
        n_locals: int,
        params_type: List[ParamType],
        code: List[CodeSegment],
        proc_usage: Union[Set[str], None] = None
    ):
        self.name = name
        self.locals_count = n_locals
        self.params_type = params_type
        self.code = code
        self.proc_usage = proc_usage

    def allocation_size(self) -> int:
        # each segment requires 2 indices
        return len(self.code) * 2 + self.locals_count
    
    def allocate_primes(self, alloc: Allocator) -> None:
        primes = alloc.allocate(self.locals_count)
        self.locals_map = {k for k in zip(range(self.locals_count), primes)}

        for c in self.code:
            c.assign_index(alloc)


# (macro) destructive move: a -> b
def move(a: AllocVar, b: AllocVar) -> CodeSegment:
    return CodeSegment([([b], [a])])


# (macro) destructive duplication: a -> b & c
def duplicate(a: AllocVar, b: AllocVar, c: AllocVar) -> CodeSegment:
    return CodeSegment([([b, c], [a])])


# (macro) move: a -> b
def copy(a: int, b: int) -> CodeSegment:
    return CodeSegment([
        ([b, 2], [a]),
        ([a], [2])
    ])
