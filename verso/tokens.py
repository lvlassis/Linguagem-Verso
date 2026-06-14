import re
from dataclasses import dataclass, replace
from enum import Enum


class TokenType(Enum):
    WEAK = 'WEAK'
    DOT = 'DOT'
    DECLARATION = 'DECLARATION'
    VARIABLE = 'VARIABLE'
    EOL = 'EOL'
    PRIMITIVE_TYPE = 'PRIMITIVE_TYPE'
    NUMERICAL_EXPRESSION = 'NUMERICAL_EXPRESSION'
    IF = 'IF'
    NOT = 'NOT'
    PRINT = 'PRINT'


class PrimitiveType(Enum):
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'



@dataclass
class Token:
    type: TokenType
    value: str | PrimitiveType | None = None


class TokenList:
    def __init__(self, tokens: list[Token] | None = None):
        self._tokens: list[Token] = tokens or []

    def find(self, tipo: TokenType) -> tuple[Token, int] | None:
        """ Retorna o primeiro token do tipo dado e seu índice, ou None """
        return next(((t, i) for i, t in enumerate(self._tokens) if t.type == tipo), None)

    def merge(self, start: int, end: int, token_type: TokenType) -> Token:
        """ Substitui tokens[start:end] por um único token com os valores concatenados """
        value = " ".join(t.value for t in self._tokens[start:end] if isinstance(t.value, str))
        merged = Token(token_type, value or None)
        self._tokens[start:end] = [merged]
        return merged

    def append(self, token: Token) -> None:
        self._tokens.append(token)

    def __iter__(self):
        return iter(self._tokens)

    def __getitem__(self, index):
        return self._tokens[index]

    def __setitem__(self, index, value):
        self._tokens[index] = value

    def __len__(self) -> int:
        return len(self._tokens)

    def __repr__(self) -> str:
        return repr(self._tokens)


def filter_comments(line: str) -> str:
    """ Remove os comentários de uma linha """
    return line.split("#")[0].strip()


def verso_split(line: str) -> list[str]:
    """ Realiza a separação inicial em uma linha """
    line = line.strip()
    words = []
    start = 0
    for i, c in enumerate(line):
        if c == " ":
            words.append(line[start:i+1])
            start = i+1
        elif c == ".":
            words.append(line[start:i])
            words.append(".")
            start = i+1
    return words


_WEAK_TOKEN_DEFINITIONS: list[tuple[str, Token]] = [
    (r"\.",                    Token(TokenType.DOT)),
    (r"é|és",                  Token(TokenType.DECLARATION)),
    (r"rocha",                 Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.INTEGER)),
    (r"digo que|gritarei",     Token(TokenType.PRINT)),
    (r"[^\s.]+",               Token(TokenType.WEAK)),
]

_TOKEN_REGEX = re.compile(
    "|".join(f"({p})" for p, _ in _WEAK_TOKEN_DEFINITIONS),
    re.IGNORECASE
)


def tokenize(program: str) -> TokenList:
    """ Função que realiza a etapa de tokenização """
    tokens = TokenList()
    for line in program.splitlines():
        line = filter_comments(line)
        line_tokens = TokenList()

        for m in _TOKEN_REGEX.finditer(line):
            group_idx = next(i for i, g in enumerate(m.groups()) if g is not None)
            template = _WEAK_TOKEN_DEFINITIONS[group_idx][1]
            token = replace(template)
            if token.type == TokenType.WEAK:
                token.value = m.group().lower()
            line_tokens.append(token)

        for token in tokenize_strong(line_tokens):
            tokens.append(token)
        tokens.append(Token(TokenType.EOL))

    return tokens


def tokenize_strong(line_tokens: TokenList) -> TokenList:
    """ Classifica os Tokens Fracos com base na sintaxe """
    tokens_classificados = [(t, i) for i, t in enumerate(line_tokens) if t.type != TokenType.WEAK]

    result = next(((t, i) for t, i in tokens_classificados if t.type == TokenType.DECLARATION), None)
    if result:
        _, pos = result
        line_tokens[pos-1].type = TokenType.VARIABLE

        if line_tokens[pos+1].type != TokenType.PRIMITIVE_TYPE:
            raise SyntaxError("Esperado token de tipo primitivo após declaração")

        if line_tokens[pos+1].value == PrimitiveType.INTEGER:
            final = line_tokens.find(TokenType.DOT) or line_tokens.find(TokenType.EOL)
            if final:
                _, i = final
                line_tokens.merge(pos+2, i, TokenType.NUMERICAL_EXPRESSION)

    return line_tokens
