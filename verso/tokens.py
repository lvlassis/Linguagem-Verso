from dataclasses import dataclass
from enum import Enum

import re
import json
from pathlib import Path

dir = Path(__file__).resolve().parent
file_path = dir / 'palavras_reservadas.json'

with open(file_path, 'r', encoding='utf-8') as file:
    PALAVRAS_RESERVADAS = json.load(file)

class TokenType(Enum):
    DOT = 'DOT'
    EOL = 'EOL'
    NUMBER = 'NUMBER'
    STRUCT = 'DATA_STRUCT'
    ELLIPSE = 'ELLIPSE'
    VARIABLE = 'VARIABLE'
    DECLARATION = 'DECLARATION'
    PRIMITIVE_TYPE = 'PRIMITIVE_TYPE'
    DATA_STRUCT = 'DATA_STRUCT'

    # Operations
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    FOR = 'FOR'

    EQUAL = 'EQUAL'
    DIFFERENT = 'DIFFERENT'
    GREATER_THAN = 'GREATER_THAN'
    LESS_THAN = 'LESS_THAN'
    GREATER_OR_EQUAL = 'GREATER_OR_EQUAL'
    LESS_OR_EQUAL = 'LESS_OR_EQUAL'

    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'

    BOOLEAN_TRUE = 'BOOLEAN_TRUE'
    BOOLEAN_FALSE = 'BOOLEAN_FALSE'

    ARTICLE = 'ARTICLE'
    PREPOSITION = 'PREPOSITION'
    CONJUNCTION = 'CONJUNCTION'


@dataclass
class Token:
    type: TokenType
    value: str | None = None


def tokenize(program: str) -> list[Token]:
    """ Função que realiza a etapa de tokenização """
    rules = [
        ('COMMENT',         r'#.*'),                  
        ('IDENTIFIER',      r'[a-zA-Z_À-ÿ][a-zA-Z0-9_À-ÿ]*'), # Captura palavras (variáveis E keywords)
        ('NUMBER',          r'\d+(\.\d+)?'),  
        ('ELLIPSE',         r'\.\.\.'),        
        ('DOT',             r'\.'),                
        ('WHITESPACE',      r'[ \t]+'),                  
        ('MISMATCH',        r'.'),
        ('EOL',             r'\n+')
    ]

    tok_regex = '|'.join(f"(?P<{name}>{rule})" for name, rule in rules)
    tokens = []

    for match in re.finditer(tok_regex, program):
        kind = match.lastgroup
        value = match.group()

        if kind in ['WHITESPACE', 'COMMENT']:
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"Erro léxico: expressão não esperada {value}")
        
        if kind == 'IDENTIFIER':
            kind = PALAVRAS_RESERVADAS.get(value, 'VARIABLE')

        tokens.append(Token(TokenType[kind], value))
    return tokens