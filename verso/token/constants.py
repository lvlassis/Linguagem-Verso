from dataclasses import dataclass, field
from enum import Enum


class TokenType(Enum):
    DOT = 'DOT'
    COMMA = 'COMMA'
    EOL = 'EOL'
    NUMBER = 'NUMBER'
    ELLIPSE = 'ELLIPSE'
    VARIABLE = 'VARIABLE'
    DECL_ATTR = 'DECL_ATTR'
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

    # Entrada
    SCAN = 'SCAN'
    
    # Operações
    SUM = 'SUM'
    SUB = 'SUB'
    MULT = 'MULT'
    DIV = 'DIV'
    REST = 'REST'


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
    "é":       Token(TokenType.DECL_ATTR),
    "és":      Token(TokenType.DECL_ATTR),
    "seja":    Token(TokenType.DECL_ATTR),
    "guarda":  Token(TokenType.DECL_ATTR),
    "encerra": Token(TokenType.DECL_ATTR),
    "guarde":  Token(TokenType.DECL_ATTR),
    "encerre": Token(TokenType.DECL_ATTR),

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

    r"acrescid[oa]s?\s+d[eao]s?":               Token(TokenType.SUM),
    r"privad[oa]s?\s+d[eao]s?":                 Token(TokenType.SUB),
    r"despid[oa]s?\s+d[eao]s?":                 Token(TokenType.SUB),
    r"ecoad[oa]s?\s+(?:por|pel[ao]s?)":         Token(TokenType.MULT),
    r"partilhad[oa]s?\s+(?:por|pel[ao]s?)":     Token(TokenType.DIV),
    r"restando\s+d[eao]s?":                     Token(TokenType.REST),
    "acresce":                                   Token(TokenType.SUM),

    "como":                         Token(TokenType.EQUAL),
    "for":                          Token(TokenType.EQUAL), 
    r"igual(\s+(a|à|ao))?":         Token(TokenType.EQUAL),
    r"diferente[s]?\s+d[eao]s?":    Token(TokenType.DIFFERENT),
    r"distint[oa]s?\s+d[eao]s?":    Token(TokenType.DIFFERENT),
    "diferente":                     Token(TokenType.DIFFERENT),
    "distinto":                      Token(TokenType.DIFFERENT),
    r"maior\s+que":                 Token(TokenType.GREATER_THAN),
    r"além\s+d[eoa]s?":             Token(TokenType.GREATER_THAN),
    "maior":                        Token(TokenType.GREATER_THAN),
    r"aquém\s+d[eoa]s?":            Token(TokenType.LESS_THAN),
    r"menor\s+que":                 Token(TokenType.LESS_THAN),
    "menor":                        Token(TokenType.LESS_THAN),
    r"até":                         Token(TokenType.LESS_OR_EQUAL),
    r"ao\s+menos":                  Token(TokenType.GREATER_OR_EQUAL),
    "me":                           Token(TokenType.GREATER_OR_EQUAL),

    "e":   Token(TokenType.AND),
    "ou":  Token(TokenType.OR),
    "não": Token(TokenType.NOT),

    "verdadeiro": Token(TokenType.BOOLEAN_TRUE, '1'),
    "falso":      Token(TokenType.BOOLEAN_FALSE, '0'),

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
    r"dig[ao](\s+que)?": Token(TokenType.PRINT),
    r"grit[eo](\s+que)?":       Token(TokenType.PRINT),
    r"gritarei(\s+que)?":    Token(TokenType.PRINT),

    r"ouç[ao](\s+(que|a|o))?": Token(TokenType.SCAN),
    r"escut[eo](\s+(o que|o|a))?":       Token(TokenType.SCAN)
}
