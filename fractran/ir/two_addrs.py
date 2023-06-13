import enum
from typing import Dict, Set, Tuple

from fractran.ir.two_addrs import Operand


class ControlFlowInfo:
    """
    Holds information regarding the control-flow of a procedure, such as
    locations of `goto` statements, etc.
    """

    labels: Dict[str, int]
    length: int

    def __init__(self, labels: Dict[str, int], code_len: int) -> None:
        self.labels = labels
        self.length = code_len


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
    
    def get_next_cfg(self, curr_line: int, info: ControlFlowInfo) -> Set[int]:
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
    
    def get_next_cfg(self, curr_line: int, info: ControlFlowInfo) -> Set[int]:
        next_line = curr_line + 1
        if next_line < info.length:
            return {next_line}
        
        return set()
