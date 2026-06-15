import re

from .constants import TokenType, PrimitiveType, Token, PALAVRAS_RESERVADAS

_RESERVED_PATTERN = '|'.join(
    fr'\b(?:{pat})\b' for pat in sorted(PALAVRAS_RESERVADAS, key=len, reverse=True)
)


def _lookup(value: str) -> Token:
    return next(entry for pat, entry in PALAVRAS_RESERVADAS.items() if re.fullmatch(pat, value))


def tokenize(program: str) -> list[Token]:
    rules = [
        ('COMMENT',    r'#.*'),
        ('RESERVED',   _RESERVED_PATTERN),
        ('IDENTIFIER', r'[a-zA-Z_À-ÿ][a-zA-Z0-9_À-ÿ]*'),
        ('NUMBER',     r'\d+(\.\d+)?'),
        ('ELLIPSE',    r'\.\.\.'),
        ('DOT',        r'\.'),
        ('COMMA'       r','),
        ('WHITESPACE', r'[ \t]+'),
        ('MISMATCH',   r'.'),
        ('EOL',        r'\n+'),
    ]

    tok_regex = '|'.join(f"(?P<{name}>{rule})" for name, rule in rules)
    tokens = []

    for match in re.finditer(tok_regex, program.lower()):
        kind = match.lastgroup
        matched = match.group()

        if kind in ('WHITESPACE', 'COMMENT'):
            continue
        if kind == 'MISMATCH':
            raise RuntimeError(f"Erro léxico: expressão não esperada {matched!r}")

        if kind == 'RESERVED':
            entry = _lookup(matched)
            token_type = entry.type
            token_value: str | PrimitiveType | None = entry.value if entry.value is not None else matched
        elif kind == 'IDENTIFIER':
            token_type = TokenType.VARIABLE
            token_value = matched
        else:
            assert kind is not None
            token_type = TokenType[kind]
            token_value = matched

        tokens.append(Token(token_type, token_value))

    return tokens
