from .code_gen import CodeSegment, Procedure, ParamType
from .var_alloc import C, L


# arithmetic procedures

# (procedure) add
ADD = Procedure(
    'add', 3, [ParamType.IN, ParamType.IN, ParamType.OUT],
    [
        CodeSegment([
            ([L(2)], [L(0)]),
            ([L(2)], [L(1)])
        ])
    ]
)

# (procedure) sub
SUB = Procedure(
    'sub', 3, [ParamType.IN, ParamType.IN, ParamType.OUT],
    [
        CodeSegment([
            ([C(1)], [L(0), L(1)]),
            ([L(2)], [L(0)]),
            ([C(1)], [L(1)])
        ])
    ]
)

# (procedure) mul
# 2: L(2)
# 3: L(0)
# 5: L(1)
# 7: L(3)
# 11: L(4)
# 13: L(5)
# 17: L(6)
MUL = Procedure(
    'mul', 7, [ParamType.IN, ParamType.IN, ParamType.OUT],
    [
        CodeSegment([
            ([L(2), L(3), L(5)], [L(1), L(4)]),
            ([L(4)], [L(5)]),
            ([C(1)], [L(4)]),
            ([L(1)], [L(3)]),
            ([L(4)], [L(0)]),
            ([C(1)], [L(1)])
        ])
    ]
)
