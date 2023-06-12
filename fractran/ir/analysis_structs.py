from typing import List, Set, Tuple


class LiveContext:
    
    length: int
    live_in: List[Set[str]]
    live_out: List[Set[str]]

    def __init__(self, length: int) -> None:
        self.length = length
        self.live_in = [set() for _ in range(self.length)]
        self.live_out = [set() for _ in range(self.length)]