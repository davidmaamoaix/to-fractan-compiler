import enum
from typing import Dict, List, Tuple

from .emit_context import EmitContext
from .var_alloc import AllocVar, C, L, Allocator


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
    locals_count: int # excluding the number of parameters
    params_type: List[ParamType]
    code: List[CodeSegment]

    # after prime allocation
    locals_map: Dict[int, int]

    def __init__(
        self,
        n_locals: int,
        params_type: List[ParamType],
        code: List[CodeSegment]
    ):
        self.locals_count = n_locals
        self.params_type = params_type
        self.code = code


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


# arithmetic procedures

# (procedure) add
ADD = Procedure(0, [ParamType.IN, ParamType.IN, ParamType.OUT], [
    ([L(2)], [L(0)]),
    ([L(2)], [L(1)])
])

# (procedure) sub
SUB = Procedure(0, [ParamType.IN, ParamType.IN, ParamType.OUT], [
    ([C(1)], [L(0), L(1)]),
    ()
])
