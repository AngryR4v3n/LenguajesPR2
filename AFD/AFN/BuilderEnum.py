from enum import Enum

class BuilderEnum(Enum):
    #del lenguaje
    SYMBOL = "SYMBOL"
    KLEENE = "α" #-> *
    PLUS = "β" #-> +
    OR = "γ" # -> |
    LEFT_PARENS = "("
    RIGHT_PARENS = ")"
    CONCAT = "δ" # -> .
    ASK = "ε" # -> ?
    HASH = "ζ"

    ALL_OPERATORS = [KLEENE, PLUS, OR, CONCAT, ASK, HASH, LEFT_PARENS, RIGHT_PARENS]