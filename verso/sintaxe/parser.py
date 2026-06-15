from verso.token.constants import Token, TokenType
from verso.sintaxe.constants import (
    SKIP_LIST, EOI_TOKEN_LIST, TYPE_TOKEN_LIST, FILLING_TOKENS_LIST, BOOLEAN_TOKENS_LIST,
    Statement, Expression, Program,
    VariableDeclaration, Attribution, Variable, Literal,
    WhileLoop, BinaryOperation, MonadicOperation, IfBody, ScanStatement,
    PrintStatement, BreakStatement, ContinueStatement, ReturnStatement,
)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self._last_eoi: TokenType | None = None

    def get_current_token(self) -> Token | None:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def get_next_token(self) -> Token | None:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def get_next_relevant_token(self) -> Token | None:
        index = 0
        while True:
            if self.pos + index >= len(self.tokens):
                break
            if self.tokens[self.pos + index].type not in SKIP_LIST:
                return self.tokens[self.pos + index]
            index += 1
        return None

    def go_to_next_relevant_token(self) -> tuple[list[Token], Token | None] | None:
        tokens = []
        while self.pos < len(self.tokens):
            if self.tokens[self.pos].type not in SKIP_LIST:
                return tokens, self.get_current_token()
            tokens.append(self.consume_token(SKIP_LIST))
        return None

    def go_to_EOI(self) -> tuple[list[Token], Token | None] | None:
        """Consome todos os tokens até chegar a um '.' ou EOL"""
        tokens = []
        while True:
            if self.pos >= len(self.tokens):
                break
            if self.tokens[self.pos].type in EOI_TOKEN_LIST:
                return tokens, self.get_current_token()
            tokens.append(self.consume_token())
        return None

    def go_to_SNI(self) -> tuple[list[Token], Token | None] | None:
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

    # --- top-level ---

    def parse_program(self) -> Program:
        instructions = []
        while self.get_current_token():
            instruction = self.parse_instructions()
            if instruction is not None:
                instructions.append(instruction)
        return Program(instructions=instructions)

    def parse_instructions(self) -> Statement | None:
        until_next_instrucion = self.go_to_SNI()
        if until_next_instrucion is None:
            return None
        _,token = self.go_to_next_relevant_token()
        if token is None:
            return None

        match token.type:
            case TokenType.IF:
                return self.parse_if()
            case TokenType.WHILE:
                return self.parse_while()
            case TokenType.PRINT:
                return self.parse_print()
            case TokenType.SCAN:
                return self.parse_scan()
            case TokenType.BREAK:
                return self.parse_break()
            case TokenType.CONTINUE:
                return self.parse_continue()
            case TokenType.RETURN:
                return self.parse_return()
            case TokenType.VARIABLE:
                next_token = self.get_next_token()
                if next_token.type != TokenType.DECL_ATTR:
                    raise SyntaxError(f"Erro sintático: expressão esperada {TokenType.DECL_ATTR}")
                return self.parse_decl_attr()
            case TokenType.EOL:
                while self.get_current_token() and self.get_current_token().type == TokenType.EOL:
                    self.consume_token()
            case TokenType.DOT:
                _ = self.go_to_SNI()
            case _:
                raise SyntaxError(f"Erro sintático: o token {self.get_next_token()} não era esperado após {token}")


        return None

    # --- control flow ---

    def parse_if(self) -> Statement:
        self.consume_token([TokenType.IF])
        condition = self.parse_expression(ignore_complements=False)
        self.consume_token([TokenType.THEN])

        instructions = []
        closed = False
        while self.get_current_token():
            while self.get_current_token() and self.get_current_token().type == TokenType.EOL:
                self.consume_token()
            if not self.get_current_token():
                break
            tok = self.get_current_token()
            if tok.type == TokenType.DOT:
                self.consume_token()
                closed = True
                break
            self._last_eoi = None
            instruction = self.parse_instructions()
            if instruction is not None:
                instructions.append(instruction)
            if self._last_eoi == TokenType.DOT:
                closed = True
                break

        if not closed:
            raise SyntaxError("Bloco IF não foi fechado")

        while self.get_current_token() and self.get_current_token().type == TokenType.EOL:
            self.consume_token()

        negative_instructions = []
        if self.get_current_token() and self.get_current_token().type == TokenType.ELSE:
            self.consume_token([TokenType.ELSE])

            while self.get_current_token() and self.get_current_token().type == TokenType.EOL:
                self.consume_token()

            closed_else = False
            while self.get_current_token():
                while self.get_current_token() and self.get_current_token().type == TokenType.EOL:
                    self.consume_token()
                if not self.get_current_token():
                    break
                tok = self.get_current_token()
                if tok.type == TokenType.DOT:
                    self.consume_token()
                    closed_else = True
                    break
                self._last_eoi = None
                instruction = self.parse_instructions()
                if instruction is not None:
                    negative_instructions.append(instruction)
                if self._last_eoi == TokenType.DOT:
                    closed_else = True
                    break

            if not closed_else:
                raise SyntaxError("Bloco ELSE não foi fechado")
        return IfBody(
            condition=condition,
            positive_instructions=instructions,
            negative_instructions=negative_instructions
        )

    def parse_while(self) -> WhileLoop:
        self.consume_token([TokenType.WHILE])
        condition = self.parse_expression(ignore_complements=False)
        body = []
        while self.get_current_token():
            while self.get_current_token() and self.get_current_token().type == TokenType.EOL:
                self.consume_token()
            if not self.get_current_token():
                break
            if self.get_current_token().type == TokenType.DOT:
                self.consume_token()
                break
            self._last_eoi = None
            instruction = self.parse_instructions()
            if instruction is not None:
                body.append(instruction)
            if self._last_eoi == TokenType.DOT:
                break

        return WhileLoop(condition=condition, body=body)

    # --- expressions ---

    def parse_expression(self, ignore_complements=True) -> Expression:
        if ignore_complements:
            _, token = self.go_to_next_relevant_token()
        else:
            token = self.get_current_token()
        if token.type == TokenType.VARIABLE or token.type in FILLING_TOKENS_LIST:
            left_node = self.parse_term()

            OPERATIONS = [
                TokenType.SUM, TokenType.SUB,
                TokenType.GREATER_THAN, TokenType.GREATER_OR_EQUAL,
                TokenType.LESS_THAN, TokenType.LESS_OR_EQUAL,
                TokenType.EQUAL, TokenType.DIFFERENT,
            ]
            while self.get_current_token() and self.get_current_token().type in OPERATIONS:
                operator = self.consume_token(OPERATIONS)
                right_node = self.parse_term()
                left_node = BinaryOperation(
                    firstOperand=left_node,
                    operator=operator,
                    SecondOperand=right_node,
                )
            return left_node

        elif token.type == TokenType.NOT:
            self.consume_token([TokenType.NOT])
            operand = self.parse_expression()
            return MonadicOperation(operand=operand, operator=token.value)
        elif token.type in BOOLEAN_TOKENS_LIST:
            self.consume_token(BOOLEAN_TOKENS_LIST)
            return Literal(token)


    def parse_term(self) -> Expression:
        left_node = self.parse_factor()

        OPERATIONS = [TokenType.MULT, TokenType.DIV, TokenType.REST]
        while self.get_current_token() and self.get_current_token().type in OPERATIONS:
            operator = self.consume_token(OPERATIONS)
            right_node = self.parse_factor()
            left_node = BinaryOperation(
                firstOperand=left_node,
                operator=operator,
                SecondOperand=right_node,
            )
        return left_node

    def parse_factor(self) -> Expression:
        token = self.get_current_token()
        if token.type == TokenType.NUMBER:
            self.consume_token()
            return Literal(value=token.value)
        elif token.type == TokenType.VARIABLE or token.type in FILLING_TOKENS_LIST:
            tokens, _ = self._go_to_nex_diff_from(TokenType.VARIABLE, ignore_complements=False)
            values = [t.value for t in tokens]
            return Literal(value=values)
        elif token.type in BOOLEAN_TOKENS_LIST:
            self.consume_token()
            return Literal(value=token)

    # --- declarations and attributions ---

    def parse_decl_attr(self) -> Statement:
        first_token = self.consume_token()
        self.consume_token()  # consome token de atribuição

        _, next_relevant_token = self.go_to_next_relevant_token()
        if next_relevant_token.type in TYPE_TOKEN_LIST:
            varType = self.consume_token()
            tokens_eoi = self.go_to_EOI()
            if tokens_eoi is None:
                raise SyntaxError("Esperado um '\\n' ou '.' ao fim da declaração.")
            value_tokens, eoi = tokens_eoi
            value = [t.value for t in value_tokens if t.type not in SKIP_LIST]
            self._last_eoi = eoi.type
            self.consume_token([eoi.type])
            return VariableDeclaration(
                name=first_token.value,
                varType=varType.value,
                value=value
            )
        else:
            tokens_eoi = self.go_to_EOI()
            if tokens_eoi is None:
                raise SyntaxError("Esperado um '\\n' ou '.' ao fim da atribuição.")
            value_tokens, eoi = tokens_eoi
            value = [t.value for t in value_tokens if t.type not in SKIP_LIST]
            self._last_eoi = eoi.type
            self.consume_token([eoi.type])
            return Attribution(
                name=first_token.value,
                value=value
            )

    # --- output and jump statements ---

    def parse_print(self) -> PrintStatement:
        self.consume_token([TokenType.PRINT])
        tok = self.get_current_token()
        if tok is None or tok.type in EOI_TOKEN_LIST:
            return PrintStatement(args=None)
        args = self.parse_expression(ignore_complements=False)
        return PrintStatement(args=args)
    
    def parse_scan(self) -> ScanStatement:
        self.consume_token([TokenType.SCAN])
        args = self.parse_expression()
        return ScanStatement(args=args)

    def parse_break(self) -> BreakStatement:
        self.consume_token([TokenType.BREAK])
        tokens = self.go_to_EOI()
        if tokens is None:
            raise SyntaxError("Espera-se um \\n ou um . ao fim da instrução. Nenhum foi fornecido.")
        
        _, EOI = tokens
        self._last_eoi = EOI.type
        self.consume_token([EOI.type])
        return BreakStatement()

    def parse_continue(self) -> ContinueStatement:
        self.consume_token([TokenType.CONTINUE])
        tokens = self.go_to_EOI()
        if tokens is None:
            raise SyntaxError("Espera-se um \\n ou um . ao fim da instrução. Nenhum foi fornecido.")
        
        _, EOI = tokens
        self._last_eoi = EOI.type
        self.consume_token([EOI.type])
        return ContinueStatement()

    def parse_return(self) -> ReturnStatement:
        self.consume_token([TokenType.RETURN])
        tokens = self.go_to_EOI()
        if tokens is None:
            raise SyntaxError("Espera-se um \\n ou um . ao fim da instrução. Nenhum foi fornecido.")
        
        value_tokens, EOI = tokens
        value = [t.value for t in value_tokens]
        self._last_eoi = EOI.type
        self.consume_token([EOI.type])
        return ReturnStatement(value=value)

    # --- helpers ---

    def _get_next_diff_from(self, tType: TokenType) -> Token | None:
        index = self.pos
        while index < len(self.tokens) and self.tokens[index].type == tType:
            index += 1
        if index < len(self.tokens):
            return self.tokens[index]
        return None

    def _go_to_nex_diff_from(self, tType: TokenType, ignore_complements=True) -> tuple[list[Token], Token | None]:
        def _run_condition():
            current_token = self.get_current_token()
            if ignore_complements:
                return current_token and current_token.type == tType
            return current_token and (current_token.type == tType or current_token.type in FILLING_TOKENS_LIST or current_token.type == TokenType.ELLIPSE)

        tokens = []
        while _run_condition():
            tokens.append(self.consume_token())
        return tokens, self.get_current_token()
