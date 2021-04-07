from enum import Enum

class BuilderEnum(Enum):
    #del lenguaje
    SYMBOL = "SYMBOL"
    KLEENE = "*"
    PLUS = "+"
    OR = "|"
    LEFT_PARENS = "("
    RIGHT_PARENS = ")"
    CONCAT = "."
    ASK = "?"