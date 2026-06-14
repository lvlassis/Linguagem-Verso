from dataclasses import dataclass
from verso.token.constants import Token, TokenType
from verso.sintaxe.constants import SKIP_LIST, EOI_TOKEN_LIST, DECL_TOKEN_LIST

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

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def get_current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def get_next_token(self) -> Token:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None
    
    def get_next_relevant_token(self) -> Token:
        index = 0

        skip_list = [
            TokenType.ARTICLE,
            TokenType.PREPOSITION,
            TokenType.CONJUNCTION
        ]

        while True:
            if self.pos + index < len(self.tokens):
                if self.tokens[self.pos + index].type not in skip_list:
                    return self.tokens[self.pos + index]
                index += 1
            else:
                break
        return None
    
    def go_to_next_relevant_token(self) -> tuple[list[Token], Token]:
        tokens = []

        while True:
            if self.pos < len(self.tokens):
                if self.tokens[self.pos].type not in SKIP_LIST:
                    return tokens, self.get_current_token()
                else:
                    tokens.append(self.consume_token(SKIP_LIST))
            else:
                break
        return None
    
    def go_to_end_of_instruction(self) -> tuple[list[Token], Token]:
        tokens = []

        while True:
            if self.pos < len(self.tokens):
                if self.tokens[self.pos].type in EOI_TOKEN_LIST:
                    return tokens, self.get_current_token()
                else:
                    tokens.append(self.consume_token())
            else:
                break
        return None
    
    def go_to_start_of_next_instruction(self) -> tuple[list[Token], Token]:

        tokens = []

        while True:
            if self.pos < len(self.tokens):
                if self.tokens[self.pos].type not in EOI_TOKEN_LIST:
                    return tokens, self.get_current_token()
                else:
                    tokens.append(self.consume_token())
            else:
                break
        return None
    
    def consume_token(self, expected_type: list[TokenType] = None) -> Token:
        token = self.get_current_token()
        if not token:
            raise SyntaxError("Fim inesperado do arquivo")
        
        if expected_type and token.type not in expected_type:
            raise SyntaxError(f"Era esperado um token do tipo {expected_type}. Foi fornecido um do tipo {token.type}.")
        
        self.pos += 1
        return token
    
    def parse_program(self) -> list[Statement]:
        instructions = []
        while True:
            if self.get_current_token() is not None:
                instruction = self.parse_instructions()
                if instruction is not None:
                    instructions.append(instruction)
            else:
                break
        return instructions

    def parse_instructions(self) -> Statement | None:
        _, token = self.go_to_next_relevant_token()


        match token.type:
            case TokenType.IF:
                pass
            case TokenType.VARIABLE:
                next_token = self.get_next_token()
                if next_token.type == TokenType.DECL_ATTR:
                    return self.parse_decl_attr()
                else:
                    raise SyntaxError(f"Erro sintático: expressão esperada {TokenType.DECL_ATTR}")
            case TokenType.EOL:
                _,_ = self.go_to_start_of_next_instruction()
            case TokenType.DOT:
                _,_ = self.go_to_start_of_next_instruction()
            
        return None
    
    def parse_decl_attr(self) -> Statement:
        first_token = self.consume_token(TokenType)
        self.consume_token() # Consome token de atribuição
        _, next_relevant_token = self.go_to_next_relevant_token()

        if next_relevant_token.type in DECL_TOKEN_LIST:
            varType = self.consume_token()
            value_tokens, EOI = self.go_to_end_of_instruction()
            values = [token.value for token in value_tokens]
            self.consume_token([EOI.type])

            return VariableDeclaration(
                name=first_token.value,
                varType=varType.value,
                value=values
            )
        elif next_relevant_token.type == TokenType.VARIABLE:
            value_tokens, EOI = self.go_to_end_of_instruction()
            values = [token.value for token in value_tokens]
            self.consume_token([EOI.type])

            return Atribuition(
                name=first_token.value,
                value=values
            )
        else :
            pass
