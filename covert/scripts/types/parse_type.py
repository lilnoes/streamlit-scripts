from enum import Enum


class ParseType(str, Enum):
    PYLATEXENC = "pylatexenc"
    SYMPY_LARK = "sympy-lark"
    SYMPY_ANTLR = "sympy-antlr"
