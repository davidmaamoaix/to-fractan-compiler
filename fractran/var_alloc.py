from typing import List


def primes(n: int) -> List[int]:
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


class AllocVar:
    """
    Represents a numeric value (always a prime) in the generated FRACTRAN code.
    Its child classes resembles 3 different possible semantics:
    - Constant: value determined during instantiation
    - Local variable: value allocated during prime allocation
    - Parameter: value allocated during prime allocation
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

    allocated_prime: int

    def assign_prime(self, prime: int):
        self.allocate_prime = prime
    
    def get_val(self) -> int:
        return self.allocated_prime
    
    
class P(AllocVar):

    param_index: int
    allocated_prime: int

    def __init__(self, param_index: int):
        self.param_index = param_index

    def assign_prime(self, prime: int):
        self.allocated_prime = prime
    
    def get_val(self) -> int:
        return self.allocated_prime
