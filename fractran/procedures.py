import enum
from typing import Set, List, Tuple

from .emit_context import EmitContext


# code segment that has yet to be mapped to concrete registers
UnmappedCodeSegment = List[Tuple[List[int], List[int]]]


class UnmappedCode:
    """
    Resembles a section of code containing unmapped instructions waiting to be
    assigned concrete registers during procedure relocation. It contains a set
    of unmapped variables and the unmapped instructions.

    Unmapped values are represented by negative integers.

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


# (macro) destructive move: a -> b
def move(a: int, b: int) -> UnmappedCode:
    return [(b, a)]


# (macro) destructive duplication: a -> b & c
def duplicate(a: int, b: int, c: int) -> UnmappedCode:
    return [(b * c, a)]


# (macro) move: a -> b
def copy(a: int, b: int) -> UnmappedCode:
    pass
