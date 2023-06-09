from typing import Dict, List, Union


# Allocation Process:
# 
# The order of prime allocation is as follows:
# 1. Program prime allocation: primes allocated for input & output variables
# 2. Code segment allocation: primes allocated for code segment indices
# 3. Pre-procedure allocation: primes allocated for local variables
#
# The above ordering is done in consideration of the string length of the
# emitted code and IO format. Input & output takes up the shortest primes, then
# the indices of code segments, then the local variables of each procedure (due
# to not being used as often).


def gen_primes(n: int) -> List[int]:
    if n <= 0:
        return []
    
    sieve = [True] * n * 20
    primes = [3]
    for i in range(5, len(sieve), 2):
        if sieve[i]:
            primes.append(i)
            if len(primes) >= n:
                return primes
            
            for j in range(i + i, len(sieve), i):
                sieve[j] = False

    return primes


class Allocator:

    index: int
    primes: List[int]

    def __init__(self, size: int):
        self.index = 0
        self.primes = gen_primes(size)

    def allocate(self, size: int) -> List[int]:
        vars = self.primes[self.index : self.index + size]
        self.index += size
        return vars
    

class VarAllocContext:

    locals_map: Dict[str, Dict[int, int]]
    procs_map: Dict[str, int]
    inputs_map: Dict[int, int]
    outputs_map: Dict[int, int]

    def __init__(
        self,
        l_map: Dict[str, Dict[int, int]],
        p_map: Dict[str, int],
        i_map: Dict[int, int],
        o_map: Dict[int, int]
    ):
        self.locals_map = l_map
        self.procs_map = p_map
        self.inputs_map = i_map
        self.outputs_map = o_map


class AllocVar:
    """
    Represents a numeric value (always a prime) in the generated FRACTRAN code.
    Its child classes resembles 4 different possible semantics:
    - Constant: value determined during instantiation
    - Local variable & parameter: value allocated during prime allocation
    - Procedure: value determined during prime allocation
    - Input & output: value determined during prime allocation
    """

    def get_val(self, _: VarAllocContext) -> int:
        raise NotImplementedError
    

# shorthands (spaghetti but explicit meh)

class C(AllocVar):

    val: int

    def __init__(self, val: int):
        self.val = val

    def get_val(self, _: VarAllocContext) -> int:
        return self.val


class L(AllocVar):

    proc_name: str
    local_index: int

    def __init__(self, proc_name: str, local_index: int):
        self.proc_name = proc_name
        self.local_index = local_index
    
    def get_val(self, ctx: VarAllocContext) -> int:
        return ctx.locals_map[self.proc_name][self.local_index]
    

class P(AllocVar):

    proc_name: str

    def __init__(self, proc_name: str):
        self.proc_name = proc_name

    def get_val(self, ctx: VarAllocContext) -> int:
        return ctx.procs_map[self.proc_name]


class I(AllocVar):

    input_index: int

    def __init__(self, input_index: int):
        self.input_index = input_index

    def get_val(self, ctx: VarAllocContext) -> int:
        return ctx.inputs_map[self.input_index]
    

class O(AllocVar):

    output_index: int

    def __init__(self, output_index: int):
        self.output_index = output_index

    def get_val(self, ctx: VarAllocContext) -> int:
        return ctx.outputs_map[self.output_index]
