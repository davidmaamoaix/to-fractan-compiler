from .code_gen import Procedure, ParamType
from .var_alloc import AllocVar, C, L, P


# arithmetic procedures

# (procedure) add
ADD = Procedure(3, [ParamType.IN, ParamType.IN, ParamType.OUT], [
    ([L(2)], [L(0)]),
    ([L(2)], [L(1)])
])

# (procedure) sub
SUB = Procedure(3, [ParamType.IN, ParamType.IN, ParamType.OUT], [
    ([C(1)], [L(0), L(1)]),
    ([L(2)], [L(0)]),
    ([C(1)], [L(1)])
])

# (procedure) mul
# 2: L(2)
# 3: L(0)
# 5: L(1)
# 7: L(3)
# 11: L(4)
# 13: L(5)
# 17: L(6)
MUL = Procedure(7, [ParamType.IN, ParamType.IN, ParamType.OUT], [
    ([L(2), L(3), L(5)], [L(1), L(4)]),
    ([L(4)], [L(5)]),
    ([C(1)], [L(4)]),
    ([L(1)], [L(3)]),
    ([L(4)], [L(0)]),
    ([C(1)], [L(1)])
])
