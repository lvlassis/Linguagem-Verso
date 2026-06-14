from enum import Enum


class TokenType(Enum):
    DOT = 'DOT'
    EOL = 'EOL'
    NUMBER = 'NUMBER'
    ELLIPSE = 'ELLIPSE'
    VARIABLE = 'VARIABLE'
    DECLARATION = 'DECLARATION'
    PRIMITIVE_TYPE = 'PRIMITIVE_TYPE'
    DATA_STRUCT = 'DATA_STRUCT'

    # Fluxo de controle
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    FOR = 'FOR'

    # Comparação
    EQUAL = 'EQUAL'
    DIFFERENT = 'DIFFERENT'
    GREATER_THAN = 'GREATER_THAN'
    LESS_THAN = 'LESS_THAN'
    GREATER_OR_EQUAL = 'GREATER_OR_EQUAL'
    LESS_OR_EQUAL = 'LESS_OR_EQUAL'

    # Lógica
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'

    # Booleanos
    BOOLEAN_TRUE = 'BOOLEAN_TRUE'
    BOOLEAN_FALSE = 'BOOLEAN_FALSE'

    # Gramaticais
    ARTICLE = 'ARTICLE'
    PREPOSITION = 'PREPOSITION'
    CONJUNCTION = 'CONJUNCTION'

    # Desvios
    CONTINUE = 'CONTINUE'
    BREAK = 'BREAK'
    RETURN = 'RETURN'

    # Saída
    PRINT = 'PRINT'


PALAVRAS_RESERVADAS: dict[str, TokenType] = {
    "é": TokenType.DECLARATION,
    "és": TokenType.DECLARATION,
    "seja": TokenType.DECLARATION,
    "guarda": TokenType.DECLARATION,
    "encerra": TokenType.DECLARATION,
    "guarde": TokenType.DECLARATION,
    "encerre": TokenType.DECLARATION,

    "rocha": TokenType.PRIMITIVE_TYPE,
    "bruma": TokenType.PRIMITIVE_TYPE,
    "névoa": TokenType.PRIMITIVE_TYPE,
    "cinza": TokenType.PRIMITIVE_TYPE,
    "dilema": TokenType.PRIMITIVE_TYPE,
    "dualidade": TokenType.PRIMITIVE_TYPE,
    "verso": TokenType.PRIMITIVE_TYPE,
    "canção": TokenType.PRIMITIVE_TYPE,
    "prosa": TokenType.PRIMITIVE_TYPE,
    "traço": TokenType.PRIMITIVE_TYPE,
    "suspiro": TokenType.PRIMITIVE_TYPE,

    "coro": TokenType.DATA_STRUCT,
    "compêndio": TokenType.DATA_STRUCT,

    "se": TokenType.IF,
    "senão": TokenType.ELSE,
    "porém": TokenType.ELSE,
    "enquanto": TokenType.WHILE,
    "sendo": TokenType.FOR,
    "então": TokenType.THEN,

    "como": TokenType.EQUAL,
    "igual": TokenType.EQUAL,
    "diferente": TokenType.DIFFERENT,
    "distinto": TokenType.DIFFERENT,
    "maior": TokenType.GREATER_THAN,
    "além": TokenType.GREATER_THAN,
    "aquém": TokenType.LESS_THAN,
    "menor": TokenType.LESS_THAN,
    "até": TokenType.LESS_OR_EQUAL,
    "me": TokenType.GREATER_OR_EQUAL,

    "e": TokenType.AND,
    "ou": TokenType.OR,
    "não": TokenType.NOT,

    "verdadeiro": TokenType.BOOLEAN_TRUE,
    "falso": TokenType.BOOLEAN_FALSE,

    "avance": TokenType.CONTINUE,
    "prossiga": TokenType.CONTINUE,
    "desista": TokenType.BREAK,
    "finde": TokenType.BREAK,
    "devolva": TokenType.RETURN,
    "entregue": TokenType.RETURN,
    "retorne": TokenType.RETURN,
    "volte": TokenType.RETURN,

    "a": TokenType.ARTICLE,
    "o": TokenType.ARTICLE,
    "um": TokenType.ARTICLE,
    "uma": TokenType.ARTICLE,

    "de": TokenType.PREPOSITION,
    "da": TokenType.PREPOSITION,

    "que": TokenType.CONJUNCTION,

    # As chaves são padrões regex — expressões multi-palavra funcionam naturalmente
    r"digo\s+que": TokenType.PRINT,
    "grito": TokenType.PRINT,
    "gritarei": TokenType.PRINT,
}
