from verso.token.constants import Token, TokenType
from verso.sintaxe.constants import (SKIP_LIST, EOI_TOKEN_LIST, TYPE_TOKEN_LIST, 
                                     Statement, Expression, Program, VariableDeclaration, Atribuition, Variable, Literal,
                                     BinaryOperation, MonadicOperation, IfBody)


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
        while True:
            if self.pos + index >= len(self.tokens):
                break

            if self.tokens[self.pos + index].type not in SKIP_LIST:
                return self.tokens[self.pos + index]
            index += 1
        return None
    
    def go_to_next_relevant_token(self) -> tuple[list[Token], Token]:
        tokens = []
        while self.pos < len(self.tokens):
            if self.tokens[self.pos].type not in SKIP_LIST:
                return tokens, self.get_current_token()
            
            tokens.append(self.consume_token(SKIP_LIST))
        return None
    
    def go_to_EOI(self) -> tuple[list[Token], Token]:
        """Consome todos os tokens até chegar à um '.' ou EOL"""

        tokens = []
        while True:
            if self.pos >= len(self.tokens):
                break

            if self.tokens[self.pos].type in EOI_TOKEN_LIST:
                return tokens, self.get_current_token()
            
            tokens.append(self.consume_token())
        return None
    
    def go_to_SNI(self) -> tuple[list[Token], Token]:
        """Consome todos os tokens até chegar ao início da próxima instrução."""

        tokens = []
        while True:
            if self.pos >= len(self.tokens):
                break

            if self.tokens[self.pos].type not in EOI_TOKEN_LIST:
                return tokens, self.get_current_token()
            else:
                tokens.append(self.consume_token())
        return None
    
    def consume_token(self, expected_type: list[TokenType] | TokenType = None) -> Token:
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
            if self.get_current_token() is None:
                break

            instruction = self.parse_instructions()
            if instruction is not None:
                instructions.append(instruction)
        return Program(instructions=instructions)

    def parse_instructions(self) -> Statement | None:
        _, token = self.go_to_next_relevant_token() # Ignora artigos

        match token.type:
            case TokenType.IF:
                next_token = self.get_next_token()
                if next_token.type != TokenType.VARIABLE:
                    raise SyntaxError(f"Erro sintático: expressão esperada {TokenType.VARIABLE}")
                return self.parse_if()
            case TokenType.VARIABLE:
                next_token = self.get_next_token()
                if next_token.type != TokenType.DECL_ATTR:
                    raise SyntaxError(f"Erro sintático: expressão esperada {TokenType.DECL_ATTR}")
                return self.parse_decl_attr()
            case TokenType.EOL:
                _ = self.go_to_SNI()
            case TokenType.DOT:
                _ = self.go_to_SNI()
            
        return None
    
    def parse_if(self) -> Statement:
        self.consume_token([TokenType.IF])
        condition = self.parse_expression()
        self.consume_token([TokenType.THEN])

        instructions = []
        while self.get_current_token() and self.get_current_token().type not in [TokenType.DOT, TokenType.ELSE]:
            instruction = self.parse_instructions()
            if instruction is not None:
                instructions.append(instruction)

        if self.get_current_token() is None or self.get_current_token().type == TokenType.ELSE:
            raise SyntaxError("Bloco IF não foi fechado")
        self.consume_token([TokenType.DOT])

        token = self.get_current_token()
        negative_instructions = []
        if token and token.type == TokenType.ELSE:
            self.consume_token([TokenType.ELSE])

            while self.get_current_token() and self.get_current_token().type != TokenType.DOT:
                instruction = self.parse_instructions()
                if instruction is not None:
                    negative_instructions.append(instruction)
            
            if self.get_current_token() is None:
                raise SyntaxError("Bloco ELIF não foi fechado")
            self.consume_token([TokenType.DOT])
        
        return IfBody(
            condition=condition,
            positive_instructions=instructions,
            negative_instructions=negative_instructions
        )

    def parse_expression(self) -> Expression:
        _, token = self.go_to_next_relevant_token()
        if token.type == TokenType.VARIABLE:
            left_node = self.parse_factor()

            OPERATIONS = [TokenType.SUM, TokenType.SUB, TokenType.GREATER_THAN, TokenType.GREATER_OR_EQUAL,
                          TokenType.LESS_THAN, TokenType.LESS_OR_EQUAL, TokenType.EQUAL, TokenType.DIFFERENT]
            while self.get_current_token() and self.get_current_token().type in OPERATIONS:
                operator = self.consume_token(OPERATIONS)
                right_node = self.parse_factor()
                left_node = BinaryOperation(firstOperand=left_node,
                                            operator=operator,
                                            SecondOperand=right_node)
            return left_node

        elif token.type == TokenType.NOT:
            self.consume_token([TokenType.NOT])

            operator = self.parse_expression()
            return MonadicOperation(
                operand=operator,
                operator=token.value
            )

    def parse_term(self) -> Expression:
        left_node = self.parse_factor()
        OPERATIONS = [TokenType.MULT, TokenType.DIV, TokenType.REST]
        while self.get_current_token() and self.get_current_token().type in OPERATIONS:
            operator = self.consume_token(OPERATIONS)
            right_node = self.parse_factor()
            left_node = BinaryOperation(firstOperand=left_node,
                                        operator=operator,
                                        SecondOperand=right_node)
        return left_node

    def parse_factor(self) -> Expression:
        token = self.get_current_token()
        if token.type == TokenType.NUMBER:
            self.consume_token()
            return Literal(value=token.value)
        elif token.type == TokenType.VARIABLE:
            tokens,_ = self._go_to_nex_diff_from(TokenType.VARIABLE)
            values = [token.value for token in tokens]
            return Literal(value=values)

    def parse_decl_attr(self) -> Statement:
        first_token = self.consume_token()
        self.consume_token() # Consome token de atribuição

        _, next_relevant_token = self.go_to_next_relevant_token()
        if next_relevant_token.type in TYPE_TOKEN_LIST:
            varType = self.consume_token()
            value_tokens, EOI = self.go_to_EOI()
            values = [token.value for token in value_tokens]

            return VariableDeclaration(
                name=first_token.value,
                varType=varType.value,
                value=values
            )
        else:
            value_tokens, EOI = self.go_to_EOI()
            values = [token.value for token in value_tokens]

            return Atribuition(
                name=first_token.value,
                value=values
            )

    def _get_next_diff_from(self, tType: TokenType) -> Token:
        index = self.pos
        while index < len(self.tokens) and self.tokens[index].type != tType:
            index += 1

        if self.tokens[index].type != tType:
            return self.tokens[index]
        return None
    
    def _get_next_diff_from(self, tType: TokenType) -> Token:
        index = self.pos
        while index < len(self.tokens) and self.tokens[index].type != tType:
            index += 1

        if self.tokens[index].type != tType:
            return self.tokens[index]
        return None
    
    def _go_to_nex_diff_from(self, tType: TokenType) -> tuple[list[Token], Token] | None:
        tokens = []
        while self.get_current_token().type == tType:
            tokens.append(self.consume_token())

        if self.get_current_token().type != tType:
            return tokens, self.get_current_token()
        return None