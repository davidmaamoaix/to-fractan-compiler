import enum
from typing import List, Tuple

from .emit_context import EmitContext


Instructions = List[Tuple[int, int]]


# reserved registers
class RRegs(enum.Enum):
    RAX = 2
    RBX = 3
    RCX = 5
    RDX = 7
    CPX = 11 # `copy` register


ADD: Instructions = [
    (2, 3),
    (2, 5)
]


# a short-hand that stores the given vars and returns their temp addresses to
# be used in a destructive operation
def preserve_vars(code: Instructions, *args):
    if len(args) > 4:
        raise RuntimeError('Cannot preserve more than 4 vars!')
    
    pairs = [zip(args, RRegs)]
    for reg, temp in pairs:
        args.extend(move(reg, temp))
    return tuple([k for k, _ in pairs])


def add(a: int, b: int, c: int, preserve: bool = True) -> Instructions:
    ins = []
    if preserve:
        a, b = preserve_vars(ins, a, b)
    
    ins.extend([(c, a), (c, b)])
    return ins


def sub(a: int, b: int, c: int, preserve: bool = True) -> Instructions:
    ins = []
    if preserve:
        a, b = preserve_vars(ins, a, b)
    
    ins.extend([(1, a * b), (c, a), (1, b)])


def mul(a: int, b: int, c: int, preserve: bool = True) -> Instructions:
    ins = []
    if preserve:
        a, b = preserve_vars(ins, a, b)
    
    ins.extend([

    ])

DIVMOD: Instructions = [
    (91, 165),
    (11, 13),
    (1, 55),
    (34, 11),
    (95, 119),
    (17, 19),
    (11, 17),
    (1, 5)
]


# destructive move: a -> b
def move(a: int, b: int) -> Instructions:
    return [(b, a)]


# destructive duplication: a -> b & c
def duplicate(a: int, b: int, c: int) -> Instructions:
    return [(b * c, a)]


# move: a -> b
def copy(a: int, b: int) -> Instructions:
    return duplicate(a, RRegs.CPX, b) + move(RRegs.CPX, a)
