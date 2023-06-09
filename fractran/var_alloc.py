from typing import List


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


class AllocVar:
    """
    Represents a numeric value (always a prime) in the generated FRACTRAN code.
    Its child classes resembles 2 different possible semantics:
    - Constant: value determined during instantiation
    - Local variable & parameter: value allocated during prime allocation
    """

    def get_val(self) -> int:
        raise NotImplementedError
    
class C(AllocVar):

    val: int

    def __init__(self, val: int):
        self.val = val

    def get_val(self) -> int:
        return self.val


class L(AllocVar):

    local_index: int
    allocated_prime: int

    def __init__(self, local_index: int):
        self.local_index = local_index
    
    def get_val(self) -> int:
        return self.allocated_prime
