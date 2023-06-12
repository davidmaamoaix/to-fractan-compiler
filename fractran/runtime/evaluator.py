import primefac
import collections
from typing import Tuple, List, Dict


def run(inp: Dict[int, int], code: List[Tuple[int, int]]) -> Dict[int, int]:
    state = 1
    for k, v in inp.items():
        state *= pow(k, v)

    while True:
        for (u, d) in code:
            if state % d == 0:
                state = state * u // d
                break
        else:
            break
    
    return collections.Counter(primefac.primefac(state))
