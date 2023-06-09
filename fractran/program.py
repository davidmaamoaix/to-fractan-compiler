from typing import Dict

from .code_gen import Procedure


class Program:

    procs: Dict[str, Procedure]

    def __init__(self):
        pass