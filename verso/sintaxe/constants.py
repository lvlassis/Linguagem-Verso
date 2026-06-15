from dataclasses import dataclass
from verso.token.constants import TokenType, PrimitiveType

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

FILLING_TOKENS_LIST = [
    TokenType.ARTICLE,
    TokenType.PREPOSITION,
    TokenType.CONJUNCTION
]

BOOLEAN_TOKENS_LIST = [
    TokenType.BOOLEAN_FALSE,
    TokenType.BOOLEAN_TRUE
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
class WhileLoop(Statement):
    condition: list
    body: list

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

@dataclass
class PrintStatement(Statement):
    args: list

@dataclass
class ScanStatement(Statement):
    args: Variable

@dataclass
class BreakStatement(Statement):
    pass

@dataclass
class ContinueStatement(Statement):
    pass

@dataclass
class ReturnStatement(Statement):
    value: list

@dataclass
class ArrayDeclaration(Statement):
    name: str
    elementType: PrimitiveType
    size: str | int | None    # palavra crua (str) antes da avaliação semântica; int depois
    values: list | None       # palavras cruas (list[str]) antes; valores avaliados depois


@dataclass
class FunctionDefinition(Statement):
    name: str
    args: list[VariableDeclaration] | None
    instructions: list[Statement]
    funcReturn: ReturnStatement

@dataclass
class FunctionCall(Expression):
    name: str
    args: list[Variable]