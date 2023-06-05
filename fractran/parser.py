import re
from parsec import *


s = regex(r'\s*', re.MULTILINE)
iden = regex(r'[_a-zA-Z][_a-zA-Z0-9]*')


