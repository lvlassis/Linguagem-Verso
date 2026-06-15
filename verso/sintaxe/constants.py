from dataclasses import dataclass
from verso.token.constants import TokenType

SKIP_LIST = [
    TokenType.ARTICLE,
    TokenType.PREPOSITION,
    TokenType.CONJUNCTION
]

EOI_TOKEN_LIST = [
            TokenType.EOL,
            TokenType.DOT,
            TokenType.COMMA
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
class Literal(Expression):
    value: str | int | float | list

@dataclass
class VariableDeclaration(Statement):
    name: str
    varType: str
    value: Expression

@dataclass
class Attribution(Statement):
    name: str
    value: Expression

@dataclass
class Variable(Expression):
    name: str

@dataclass
class BinaryOperation(Expression):
    firstOperand: Expression
    operator: str
    SecondOperand: Expression

@dataclass
class MonadicOperation(Expression):
    operand: Expression
    operator: str

@dataclass
class IfBody(Statement):
    condition: Expression
    positive_instructions: list[Statement]
    negative_instructions: list[Statement]