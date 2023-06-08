import enum
from typing import Set, List, Tuple

from .emit_context import EmitContext


UnmappedCodeSegment = List[Tuple[int, int]]


class ParamType(enum):
    IN = 0
    OUT = 1


class UnmappedCode:
    """
    Resembles a section of code containing unmapped instructions waiting to be
    assigned concrete registers during procedure relocation. It contains a set
    of unmapped variables (local variables) and the unmapped instructions.

    Unmapped values are represented by negative integers. Each negative number
    is local to its `UnmappedCode`.

    Each tuple contains two lists: nominator and denominator. After mapping
    negative values to concrete primes, the product of each list becomes the
    nominator and denominator respectively.
    """

    remap: Set[int]
    instructions: UnmappedCodeSegment

    def __init__(self, code: UnmappedCodeSegment):
        self.instructions = code
        self.remap = set.union(*[{i for i in n + d if i < 0} for n, d in code])

    def unmap_size(self) -> int:
        return len(self.remap)
    

class Procedure:

    # on initialization
    locals_count: int
    params_type: List[ParamType]
    code: List[UnmappedCode]

    # after prime allocation
    index: int
    params_index: List[int]

    def __init__(self, code: List[UnmappedCode]):
        pass
        


# (macro) destructive move: a -> b
def move(a: int, b: int) -> UnmappedCode:
    return UnmappedCode([([b], [a])])


# (macro) destructive duplication: a -> b & c
def duplicate(a: int, b: int, c: int) -> UnmappedCode:
    return UnmappedCode([([b, c], [a])])


# (macro) move: a -> b
def copy(a: int, b: int) -> UnmappedCode:
    return UnmappedCode([
        ([b, 2], [a]),
        ([a], [2])
    ])
