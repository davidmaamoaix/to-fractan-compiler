from typing import List, Tuple

from .emit_context import EmitContext


Instructions = List[Tuple[int, int]]

ADD: Instructions = [
    (2, 3),
    (2, 5)
]

SUB: Instructions = [
    (1, 15),
    (2, 3),
    (1, 5)
]

MUL: Instructions = [
    (182, 55),
    (11, 13),
    (1, 11),
    (5, 7),
    (11, 3),
    (1, 5)
]

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
    pass
