import enum
from typing import Dict, List, Set, Tuple

from fractran.ir.two_addrs import ControlFlowInfo, Operand


class ParamType(enum.Enum):
    IN = 0
    OUT = 1


class ProcedureInfo:
    """
    Holds information regarding the attributes of a procedure, such as locations
    of `goto` statements, etc.
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
    
    def get_used_locals(self) -> Set[str]:
        return set()
    

class Constant(Operand):

    value: int

    def __init__(self, value: int) -> None:
        self.value = value


class LocalVar(Operand):
    
    proc_name: str
    index: int

    def __init__(self, proc_name: str, index: int) -> None:
        self.proc_name = proc_name
        self.index = index

    def get_used_locals(self) -> Set[str]:
        return {self.proc_name}


class IOVar(Operand):

    is_output: bool
    index: int

    def __init__(self, is_output: bool, index: int) -> None:
        self.is_output = is_output
        self.index = index


class IRCode:
    
    def get_live_locals(self) -> Set[str]:
        return set()
    
    def get_unlive_locals(self) -> Set[str]:
        return set()
    
    def get_next_cfg(self, curr_line: int, info: ControlFlowInfo) -> Set[int]:
        raise NotImplementedError
    

class GoToCode(IRCode):

    label: str

    def __init__(self, label: str) -> None:
        self.label = label

    def get_next_cfg(self, curr_line: int, info: ControlFlowInfo) -> Set[int]:
        return {info.labels[self.label]}
    

class GoToIfCode(IRCode):

    expr: Operand
    label: str

    def __init__(self, expr: Operand, label: str) -> None:
        self.expr = expr
        self.label = label

    def get_live_locals(self) -> Set[str]:
        return self.expr.get_used_locals()

    def get_next_cfg(self, curr_line: int, info: ControlFlowInfo) -> Set[int]:
        jump_line = {info.labels[self.label]}

        if curr_line + 1 < info.length:
            jump_line.add(curr_line + 1)

        return jump_line


class TwoAddrCode(IRCode):

    lhs: Operand
    oper: OpCode
    rhs: Operand

    def __init__(self, lhs: Operand, oper: OpCode, rhs: Operand) -> None:
        self.lhs = lhs
        self.oper = oper
        self.rhs = rhs

    def get_live_locals(self) -> Set[str]:
        vars = self.rhs.get_used_locals()
        if self.oper != OpCode.MOV:
            vars.update(self.lhs.get_used_locals())
        
        return vars
    
    def get_unlive_locals(self) -> Set[str]:
        if self.oper == OpCode.MOV:
            return self.lhs.get_used_locals()

        return set()
    
    def get_next_cfg(self, curr_line: int, info: ControlFlowInfo) -> Set[int]:
        next_line = curr_line + 1
        if next_line < info.length:
            return {next_line}
        
        return set()


class ProcedureIR:

    name: str
    params: List[str]
    params_type: Dict[str, ParamType]
    code: List[IRCode]

    def __init__(
        self,
        name: str,
        params: List[str],
        params_type: Dict[str, ParamType],
        code: List[IRCode]
    ) -> None:
        self.name = name
        self.params = params
        self.params_type = params_type
        self.code = code
