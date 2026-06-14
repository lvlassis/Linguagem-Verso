from dataclasses import dataclass
from enum import Enum
import re

PALAVRAS_RESERVADAS = {
    'é': 'DECLARATION',
    'rocha': 'PRIMITIVE_TYPE',
    'bruma': 'PRIMITIVE_TYPE',
    'cinza': 'PRIMITIVA_TYPE'
}

class TokenType(Enum):
    DOT = 'DOT'
    EOL = 'EOL'
    VARIABLE = 'VARIABLE'
    DECLARATION = 'DECLARATION'
    PRIMITIVE_TYPE = 'PRIMITIVE_TYPE'
    NUMBER = 'NUMBER'
    ELLIPSE = 'ELLIPSE'


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