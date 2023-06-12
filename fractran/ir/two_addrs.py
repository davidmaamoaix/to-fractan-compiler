import enum
from typing import List, Set, Tuple

from fractran.ir.two_addrs import Operand


class OpCode(enum.Enum):
    MOV = enum.auto()
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()
    MOD = enum.auto()


class Operand:
    pass


class IRCode:
    
    def get_live_vars(self) -> Set[Operand]:
        raise NotImplementedError


class TwoAddrCode(IRCode):

    lhs: Operand
    oper: OpCode
    rhs: Operand

    def __init__(self, lhs: Operand, oper: OpCode, rhs: Operand) -> None:
        self.lhs = lhs
        self.oper = oper
        self.rhs = rhs

    def get_live_vars(self) -> Set[Operand]:
        return {self.rhs}
