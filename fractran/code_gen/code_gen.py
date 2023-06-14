import enum
import functools
from typing import Dict, List, Set, Tuple, Union

from .var_alloc import AllocVar, VarAllocContext, C
from ..ir.two_addrs import ParamType


FracCode = List[Tuple[List[AllocVar], List[AllocVar]]]


class CodeSegment:
    
    # on initialization
    code: FracCode

    # after prime allocation
    index: Tuple[int, int]

    def __init__(self, code: FracCode):
        self.code = code

    def get_entry_index(self) -> int:
        return self.index[0]
    
    def code_gen(
        self,
        ctx: VarAllocContext,
        next_segment_index: int = 1
    ) -> List[Tuple[int, int]]:
        target_code: List[Tuple[int, int]] = []
        for ns, ds in self.code:
            n = functools.reduce(lambda a, b: a * b.get_val(ctx), ns, 1)
            d = functools.reduce(lambda a, b: a * b.get_val(ctx), ds, 1)
            target_code.append((n, d))
        
        # segment index (header and footer)
        target_code.insert(0, (self.index[1], self.index[0]))
        target_code.append((next_segment_index, self.index[1]))

        return target_code


class Procedure:

    name: str
    n_locals: int # including the number of parameters
    params_type: List[ParamType]
    code: List[CodeSegment]
    proc_usage: Set[str]

    def __init__(
        self,
        name: str,
        n_locals: int,
        params_type: List[ParamType],
        code: List[CodeSegment],
        proc_usage: Union[Set[str], None] = None
    ):
        self.name = name
        self.n_locals = n_locals
        self.params_type = params_type
        self.code = code
        self.proc_usage = proc_usage if proc_usage else set()
    
    def set_seg_indices(self, indices: List[int]) -> int:
        """
        Sets the code segment indices for all code segments in this procedure.
        Returns the starting index of this procedure (set the flag to invoke
        this procedure).
        """

        for i, segment in zip(range(0, len(indices), 2), self.code):
            segment.index = (indices[i], indices[i + 1])

        return indices[0]
    
    def code_gen(self, ctx: VarAllocContext) -> List[Tuple[int, int]]:
        pass


# (macro) destructive move: a -> b
def move(a: AllocVar, b: AllocVar) -> List[CodeSegment]:
    return [CodeSegment([([b], [a])])]


# (macro) destructive duplication: a -> b & c
def duplicate(a: AllocVar, b: AllocVar, c: AllocVar) -> List[CodeSegment]:
    return [CodeSegment([([b, c], [a])])]


# (macro) move: a -> b
def copy(a: AllocVar, b: AllocVar) -> List[CodeSegment]:
    return [
        CodeSegment([
            ([b, C(2)], [a])
        ]),
        CodeSegment([
            ([a], [C(2)])
        ])
    ]
