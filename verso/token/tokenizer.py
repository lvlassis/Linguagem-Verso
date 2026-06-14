import re

from .constants import TokenType, PALAVRAS_RESERVADAS
from .model import Token

# Padrões ordenados do mais longo para o mais curto para garantir que
# palavras mais específicas (ex: "senão") sejam tentadas antes das mais
# curtas que as contêm (ex: "se").
# \b é Unicode-aware no Python 3: reconhece letras acentuadas como parte
# de palavra, equivalente ao \<...\> do Vim.
_RESERVED_PATTERN = '|'.join(
    fr'\b(?:{pat})\b' for pat in sorted(PALAVRAS_RESERVADAS, key=len, reverse=True)
)


def _lookup(value: str) -> TokenType:
    return next(tt for pat, tt in PALAVRAS_RESERVADAS.items() if re.fullmatch(pat, value))


def tokenize(program: str) -> list[Token]:
    rules = [
        ('COMMENT',    r'#.*'),
        ('RESERVED',   _RESERVED_PATTERN),
        ('IDENTIFIER', r'[a-zA-Z_À-ÿ][a-zA-Z0-9_À-ÿ]*'),
        ('NUMBER',     r'\d+(\.\d+)?'),
        ('ELLIPSE',    r'\.\.\.'),
        ('DOT',        r'\.'),
        ('WHITESPACE', r'[ \t]+'),
        ('MISMATCH',   r'.'),
        ('EOL',        r'\n+'),
    ]

    tok_regex = '|'.join(f"(?P<{name}>{rule})" for name, rule in rules)
    tokens = []

    for match in re.finditer(tok_regex, program.lower()):
        kind = match.lastgroup
        value = match.group()

        if kind in ('WHITESPACE', 'COMMENT'):
            continue
        if kind == 'MISMATCH':
            raise RuntimeError(f"Erro léxico: expressão não esperada {value!r}")

        if kind == 'RESERVED':
            token_type = _lookup(value)
        elif kind == 'IDENTIFIER':
            token_type = TokenType.VARIABLE
        else:
            assert kind is not None
            token_type = TokenType[kind]

        tokens.append(Token(token_type, value))

    return tokens
