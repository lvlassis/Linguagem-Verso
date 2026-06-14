from dataclasses import dataclass, field
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


class PrimitiveType(Enum):
    INTEGER = 'INTEGER'
    FLOAT   = 'FLOAT'
    CHAR    = 'CHAR'
    STRING  = 'STRING'
    BOOL    = 'BOOL'


@dataclass
class Token:
    type: TokenType
    value: str | PrimitiveType | None = field(default=None)


PALAVRAS_RESERVADAS: dict[str, Token] = {
    "é":       Token(TokenType.DECLARATION),
    "és":      Token(TokenType.DECLARATION),
    "seja":    Token(TokenType.DECLARATION),
    "guarda":  Token(TokenType.DECLARATION),
    "encerra": Token(TokenType.DECLARATION),
    "guarde":  Token(TokenType.DECLARATION),
    "encerre": Token(TokenType.DECLARATION),

    "rocha":     Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.INTEGER),
    "bruma":     Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.FLOAT),
    "névoa":     Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.FLOAT),
    "cinza":     Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.FLOAT),
    "traço":     Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.CHAR),
    "suspiro":   Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.CHAR),
    "verso":     Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.STRING),
    "canção":    Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.STRING),
    "prosa":     Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.STRING),
    "dilema":    Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.BOOL),
    "dualidade": Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.BOOL),

    "coro":      Token(TokenType.DATA_STRUCT),
    "compêndio": Token(TokenType.DATA_STRUCT),

    "se":       Token(TokenType.IF),
    "senão":    Token(TokenType.ELSE),
    "porém":    Token(TokenType.ELSE),
    "enquanto": Token(TokenType.WHILE),
    "sendo":    Token(TokenType.FOR),
    "então":    Token(TokenType.THEN),

    "como":      Token(TokenType.EQUAL),
    "igual":     Token(TokenType.EQUAL),
    "diferente": Token(TokenType.DIFFERENT),
    "distinto":  Token(TokenType.DIFFERENT),
    "maior":     Token(TokenType.GREATER_THAN),
    "além":      Token(TokenType.GREATER_THAN),
    "aquém":     Token(TokenType.LESS_THAN),
    "menor":     Token(TokenType.LESS_THAN),
    "até":       Token(TokenType.LESS_OR_EQUAL),
    "me":        Token(TokenType.GREATER_OR_EQUAL),

    "e":   Token(TokenType.AND),
    "ou":  Token(TokenType.OR),
    "não": Token(TokenType.NOT),

    "verdadeiro": Token(TokenType.BOOLEAN_TRUE),
    "falso":      Token(TokenType.BOOLEAN_FALSE),

    "avance":   Token(TokenType.CONTINUE),
    "prossiga": Token(TokenType.CONTINUE),
    "desista":  Token(TokenType.BREAK),
    "finde":    Token(TokenType.BREAK),
    "devolva":  Token(TokenType.RETURN),
    "entregue": Token(TokenType.RETURN),
    "retorne":  Token(TokenType.RETURN),
    "volte":    Token(TokenType.RETURN),

    "a":   Token(TokenType.ARTICLE),
    "o":   Token(TokenType.ARTICLE),
    "um":  Token(TokenType.ARTICLE),
    "uma": Token(TokenType.ARTICLE),

    "de": Token(TokenType.PREPOSITION),
    "da": Token(TokenType.PREPOSITION),

    "que": Token(TokenType.CONJUNCTION),

    # As chaves são padrões regex — expressões multi-palavra funcionam naturalmente
    r"digo\s+que": Token(TokenType.PRINT),
    "grito":       Token(TokenType.PRINT),
    "gritarei":    Token(TokenType.PRINT),
}
