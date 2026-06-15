from verso.token.constants import TokenType
from dataclasses import dataclass

SKIP_LIST = [
            TokenType.ARTICLE,
            TokenType.PREPOSITION,
            TokenType.CONJUNCTION
        ]

EOI_TOKEN_LIST = [
            TokenType.EOL,
            TokenType.DOT
        ]

TYPE_TOKEN_LIST = [
    TokenType.PRIMITIVE_TYPE,
    TokenType.DATA_STRUCT
]

class ASTNode:
    pass
class Statement(ASTNode):
    pass
class Expression(ASTNode):
    pass

@dataclass
class Program(ASTNode):
    instructions: list[Statement]

@dataclass
class VariableDeclaration(Statement):
    name: str
    varType: str
    value: list[str]

@dataclass
class Atribuition(Statement):
    name: str
    value: list[str]

@dataclass
class Literal(Expression):
    value: str

@dataclass
class Variable(Expression):
    name: str