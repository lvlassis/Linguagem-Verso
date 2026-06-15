from verso.token.constants import Token, TokenType
from verso.sintaxe.constants import (
    SKIP_LIST, EOI_TOKEN_LIST, TYPE_TOKEN_LIST,
    Statement, Expression, Program,
    VariableDeclaration, Attribution, WhileLoop,
    PrintStatement, BreakStatement, ContinueStatement, ReturnStatement,
)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self._last_eoi: TokenType | None = None

    def get_current_token(self) -> Token|None:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def get_next_token(self) -> Token|None:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None
    
    def get_next_relevant_token(self) -> Token|None:
        index = 0
        while True:
            if self.pos + index >= len(self.tokens):
                break

            if self.tokens[self.pos + index].type not in SKIP_LIST:
                return self.tokens[self.pos + index]
            index += 1
        return None
    
    def go_to_next_relevant_token(self) -> tuple[list[Token], Token|None]|None:
        tokens = []
        while True:
            if self.pos >= len(self.tokens):
                break

            if self.tokens[self.pos].type not in SKIP_LIST:
                return tokens, self.get_current_token()
            
            tokens.append(self.consume_token(SKIP_LIST))
        return None
    
    def go_to_EOI(self) -> tuple[list[Token], Token|None]|None:
        """Consome todos os tokens até chegar à um '.' ou EOL"""

        tokens = []
        while True:
            if self.pos >= len(self.tokens):
                break

            if self.tokens[self.pos].type in EOI_TOKEN_LIST:
                return tokens, self.get_current_token()
            
            tokens.append(self.consume_token())
        return None
    
    def go_to_SNI(self) -> tuple[list[Token], Token|None]|None:
        """Consome todos os tokens até chegar ao início da próxima instrução."""

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
    
    def consume_token(self, expected_type: list[TokenType]|None= None) -> Token:
        token = self.get_current_token()
        if not token:
            raise SyntaxError("Fim inesperado do arquivo")
        
        if expected_type and token.type not in expected_type:
            raise SyntaxError(f"Era esperado um token do tipo {expected_type}. Foi fornecido um do tipo {token.type}.")
        
        self.pos += 1
        return token
    
    def parse_program(self) -> Program:
        instructions = []
        while self.get_current_token():
            instruction = self.parse_instructions()
            if instruction is not None:
                instructions.append(instruction)
        return Program(instructions=instructions)

    def parse_instructions(self) -> Statement | None:
        _, token = self.go_to_next_relevant_token() # Ignora artigos

        match token.type:
            case TokenType.IF:
                pass
            case TokenType.WHILE:
                return self.parse_while()
            case TokenType.PRINT:
                return self.parse_print()
            case TokenType.BREAK:
                return self.parse_break()
            case TokenType.CONTINUE:
                return self.parse_continue()
            case TokenType.RETURN:
                return self.parse_return()
            case TokenType.VARIABLE:
                next_token = self.get_next_token()
                if next_token.type == TokenType.DECL_ATTR:
                    return self.parse_decl_attr()
                else:
                    raise SyntaxError(f"Erro sintático: expressão esperada {TokenType.DECL_ATTR}")
            case TokenType.EOL:
                self.go_to_SNI()
            case TokenType.DOT:
                self.go_to_SNI()

        return None
    
    def parse_decl_attr(self) -> Statement:
        first_token = self.consume_token(TokenType)
        self.consume_token() # Consome token de atribuição

        _, next_relevant_token = self.go_to_next_relevant_token()
        if next_relevant_token.type in TYPE_TOKEN_LIST:
            varType = self.consume_token()
            value_tokens, EOI = self.go_to_EOI()
            values = [token.value for token in value_tokens]
            self._last_eoi = EOI.type
            self.consume_token([EOI.type])

            return VariableDeclaration(
                name=first_token.value,
                varType=varType.value,
                value=values
            )
        else:
            value_tokens, EOI = self.go_to_EOI()
            values = [token.value for token in value_tokens]
            self._last_eoi = EOI.type
            self.consume_token([EOI.type])

            return Attribution(
                name=first_token.value,
                value=values
            )

    def parse_print(self) -> PrintStatement:
        self.consume_token([TokenType.PRINT])
        value_tokens, EOI = self.go_to_EOI()
        args = [t.value for t in value_tokens]
        self._last_eoi = EOI.type
        self.consume_token([EOI.type])
        return PrintStatement(args=args)

    def parse_break(self) -> BreakStatement:
        self.consume_token([TokenType.BREAK])
        _, EOI = self.go_to_EOI()
        self._last_eoi = EOI.type
        self.consume_token([EOI.type])
        return BreakStatement()

    def parse_continue(self) -> ContinueStatement:
        self.consume_token([TokenType.CONTINUE])
        _, EOI = self.go_to_EOI()
        self._last_eoi = EOI.type
        self.consume_token([EOI.type])
        return ContinueStatement()

    def parse_return(self) -> ReturnStatement:
        self.consume_token([TokenType.RETURN])
        value_tokens, EOI = self.go_to_EOI()
        value = [t.value for t in value_tokens]
        self._last_eoi = EOI.type
        self.consume_token([EOI.type])
        return ReturnStatement(value=value)

    def parse_while(self) -> WhileLoop:
        self.consume_token([TokenType.WHILE])

        condition_tokens, eoi = self.go_to_EOI()
        condition = [t for t in condition_tokens if t.type not in SKIP_LIST]
        self.consume_token([eoi.type])
        self.go_to_SNI()

        body = []
        while self.get_current_token():
            if self.get_current_token().type == TokenType.DOT:
                self.go_to_SNI()
                break
            self._last_eoi = None
            instruction = self.parse_instructions()
            if instruction is not None:
                body.append(instruction)
            if self._last_eoi == TokenType.DOT:
                break

        return WhileLoop(condition=condition, body=body)
