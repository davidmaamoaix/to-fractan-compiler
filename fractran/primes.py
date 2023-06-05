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
