import enum
from typing import Dict, List, Set, Tuple, Union

from .var_alloc import AllocVar, C


FracCode = List[Tuple[List[AllocVar], List[AllocVar]]]


class ParamType(enum.Enum):
    IN = 0
    OUT = 1


class CodeSegment:
    
    # on initialization
    code: FracCode

    # after prime allocation
    index: Tuple[int, int]

    def __init__(self, code: FracCode):
        self.code = code

    def assign_index(self, index: Tuple[int, int]) -> None:
        self.index = index


class Procedure:

    # on initialization
    name: str
    n_locals: int # including the number of parameters
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
        self.n_locals = n_locals
        self.params_type = params_type
        self.code = code
        self.proc_usage = proc_usage if proc_usage else set()

    def locals_size(self) -> int:
        return self.n_locals

    def index_size(self) -> int:
        # each segment requires 2 indices
        return 2 * len(self.code)
    
    def set_seg_indices(self, indices: List[int]) -> int:
        """
        Sets the code segment indices for all code segments in this procedure.
        Returns the starting index of this procedure (set the flag to invoke
        this procedure).
        """

        for i, segment in zip(range(0, len(indices), 2), self.code):
            segment.assign_index((indices[i], indices[i + 1]))

        return indices[0]


# (macro) destructive move: a -> b
def move(a: AllocVar, b: AllocVar) -> CodeSegment:
    return CodeSegment([([b], [a])])


# (macro) destructive duplication: a -> b & c
def duplicate(a: AllocVar, b: AllocVar, c: AllocVar) -> CodeSegment:
    return CodeSegment([([b, c], [a])])


# (macro) move: a -> b
def copy(a: AllocVar, b: AllocVar) -> CodeSegment:
    return CodeSegment([
        ([b, C(2)], [a]),
        ([a], [C(2)])
    ])
