from typing import Dict, List, Union

from fractran.var_alloc import CodeGenContext

# Allocation Process:
# 
# The order of prime allocation is as follows:
# 1. Program prime allocation: primes allocated for input & output variables
# 2. Pre-procedure allocation: primes allocated for local variables
# 3. Procedure allocation: primes allocated for procedure indices
# 4. Post-procedure linking: `P` placeholders gets their value populated
#
# The above ordering is done in consideration of the string length of the
# emitted code and IO format. Input & output takes up the shortest primes, then
# 


def gen_primes(n: int) -> List[int]:
    if n <= 0:
        return []
    
    sieve = [True] * n * 20
    primes = [2]
    for i in range(3, len(sieve), 2):
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

    def __init__(self, size):
        self.index = 0
        self.primes = gen_primes(size)

    def allocate(self, size: int) -> List[int]:
        vars = self.primes[self.index : self.index + size]
        self.index += size
        return vars
    

class CodeGenContext:

    locals_map: Union[Dict[int, int], None]
    procs_map: Dict[str, int]
    inputs_map: Dict[int, int]
    outputs_map: Dict[int, int]

    def __init__(
        self,
        p_map: Dict[str, int],
        i_map: Dict[str, int],
        o_map: Dict[str, int]
    ):
        self.locals_map = None
        self.procs_map = p_map
        self.inputs_map = i_map
        self.outputs_map = o_map

    def set_locals_map(self, l_map: Dict[int, int]) -> None:
        self.locals_map = l_map


class AllocVar:
    """
    Represents a numeric value (always a prime) in the generated FRACTRAN code.
    Its child classes resembles 4 different possible semantics:
    - Constant: value determined during instantiation
    - Local variable & parameter: value allocated during prime allocation
    - Procedure: value determined AFTER instantiation
    - IO
    """

    def get_val(self, ctx: CodeGenContext) -> int:
        raise NotImplementedError
    
# shorthands (spaghetti but explicit meh)

class C(AllocVar):

    val: int

    def __init__(self, val: int):
        self.val = val

    def get_val(self, _: CodeGenContext) -> int:
        return self.val


class L(AllocVar):

    local_index: int

    def __init__(self, local_index: int):
        self.local_index = local_index
    
    def get_val(self, ctx: CodeGenContext) -> int:
        return ctx.locals_map[self.local_index]
    

class P(AllocVar):

    proc_name: str

    def __init__(self, proc_name: str):
        self.proc_name = proc_name

    def get_val(self, ctx: CodeGenContext) -> int:
        return ctx.procs_map[self.proc_name]


class I(AllocVar):

    input_index: int

    def __init__(self, input_index: int):
        self.input_index = input_index

    def get_val(self, ctx: CodeGenContext) -> int:
        return ctx.inputs_map[self.input_index]
    

class O(AllocVar):

    output_index: int

    def __init__(self, output_index: int):
        self.output_index = output_index

    def get_val(self, ctx: CodeGenContext) -> int:
        return ctx.outputs_map[self.output_index]
