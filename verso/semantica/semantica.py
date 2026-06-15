from verso.semantica.constants import SemanticError
from verso.ast import (
    Program, Statement, Expression,
    VariableDeclaration, Attribution, WhileLoop, IfBody,
    PrintStatement, BreakStatement, ContinueStatement, ReturnStatement,
    BinaryOperation, MonadicOperation, Literal,
)
from verso.token.constants import PrimitiveType, TokenType, Token

_OPERADORES_COMPARACAO = frozenset({
    TokenType.EQUAL, TokenType.DIFFERENT,
    TokenType.GREATER_THAN, TokenType.LESS_THAN,
    TokenType.GREATER_OR_EQUAL, TokenType.LESS_OR_EQUAL,
})
_OPERADORES_LOGICOS = frozenset({TokenType.AND, TokenType.OR})
_OPERADORES_ARITMETICOS = frozenset({
    TokenType.SUM, TokenType.SUB, TokenType.MULT, TokenType.DIV, TokenType.REST,
})
_TIPOS_NUMERICOS = frozenset({PrimitiveType.INTEGER, PrimitiveType.FLOAT})


class SemanticAnalyzer:
    def __init__(self) -> None:
        self._scopes: list[dict[str, PrimitiveType]] = [{}]

    # --- scope helpers ---

    def _push_scope(self) -> None:
        self._scopes.append({})

    def _pop_scope(self) -> None:
        if len(self._scopes) > 1:
            self._scopes.pop()

    def _declare(self, name: str, varType: PrimitiveType) -> None:
        self._scopes[-1][name] = varType

    def _lookup(self, name: str) -> PrimitiveType | None:
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None

    def _is_declared(self, name: str) -> bool:
        return self._lookup(name) is not None

    @staticmethod
    def _is_numeric_literal(val: str) -> bool:
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False

    # --- public API ---

    def analyse(self, tree: Program) -> tuple[Program, list[SemanticError] | None]:
        errors = []
        for instruction in tree.instructions:
            errors += self._visit(instruction)
        return tree, errors or None

    # --- visitors ---

    def _visit(self, node: Statement) -> list[SemanticError]:
        match node:
            case VariableDeclaration():
                print(node)
                return self._visit_declaration(node)
            case Attribution():
                return self._visit_attribution(node)
            case WhileLoop():
                return self._visit_while(node)
            case IfBody():
                return self._visit_if(node)
            case PrintStatement():
                return self._visit_print(node)
            case BreakStatement() | ContinueStatement():
                return []
            case ReturnStatement():
                return self._visit_return(node)
        return []

    def _visit_declaration(self, node: VariableDeclaration) -> list[SemanticError]:
        if node.name in self._scopes[-1]:
            return [SemanticError(f"'{node.name}' já foi declarada.")]

        self._declare(node.name, node.varType)

        if node.value:
            if node.varType == PrimitiveType.INTEGER:
                node.value = [self._avaliar_expressao_int(node.value)]
            elif node.varType == PrimitiveType.FLOAT:
                node.value = [self._avaliar_expressao_float(node.value)]
            else:
                return self._validar_valor(node.name, node.varType, node.value)

        return []

    def _visit_attribution(self, node: Attribution) -> list[SemanticError]:
        if not self._is_declared(node.name):
            return [SemanticError(f"'{node.name}' não foi declarada.")]

        declared_type = self._lookup(node.name)
        palavras = [v for v in node.value if isinstance(v, str)]
        expressoes = [p for p in palavras if not self._is_declared(p) and not self._is_numeric_literal(p)]

        if expressoes:
            if declared_type == PrimitiveType.INTEGER:
                node.value = [self._avaliar_expressao_int(node.value)]
                return []
            elif declared_type == PrimitiveType.FLOAT:
                node.value = [self._avaliar_expressao_float(node.value)]
                return []

        return self._validar_valor(node.name, declared_type, node.value)

    def _validar_valor(self, varname: str, declared_type: PrimitiveType, value: list) -> list[SemanticError]:
        palavras = [v for v in value if isinstance(v, str)]
        variaveis  = [p for p in palavras if self._is_declared(p)]
        expressoes = [p for p in palavras if not self._is_declared(p) and not self._is_numeric_literal(p)]

        if expressoes:
            return [SemanticError(f"'{expressoes[0]}' não foi declarada.")]

        errors = []
        for val in variaveis:
            val_type = self._lookup(val)
            if val_type != declared_type:
                errors.append(SemanticError(
                    f"Tipo incompatível: '{val}' é {val_type.value}, "
                    f"mas '{varname}' espera {declared_type.value}."
                ))
        return errors

    def _visit_if(self, node: IfBody) -> list[SemanticError]:
        _, errors = self._verificar_expressao(node.condition)

        self._push_scope()
        for stmt in node.positive_instructions:
            errors += self._visit(stmt)
        self._pop_scope()
        if node.negative_instructions:
            self._push_scope()
            for stmt in node.negative_instructions:
                errors += self._visit(stmt)
            self._pop_scope()
        return errors

    def _visit_while(self, node: WhileLoop) -> list[SemanticError]:
        _, errors = self._verificar_expressao(node.condition)

        self._push_scope()
        for stmt in node.body:
            errors += self._visit(stmt)
        self._pop_scope()
        return errors

    def _verificar_expressao(self, node: Expression) -> tuple[PrimitiveType | None, list[SemanticError]]:
        match node:
            case Literal():
                if isinstance(node.value, Token):
                    return PrimitiveType.BOOL, []
                if isinstance(node.value, list):
                    errors, tipo = [], None
                    for nome in node.value:
                        if not self._is_declared(nome):
                            errors.append(SemanticError(f"'{nome}' não foi declarada."))
                        elif tipo is None:
                            tipo = self._lookup(nome)
                    return tipo, errors
                val = str(node.value)
                return (PrimitiveType.FLOAT if '.' in val else PrimitiveType.INTEGER), []

            case BinaryOperation():
                tipo_esq, erros_esq = self._verificar_expressao(node.firstOperand)
                tipo_dir, erros_dir = self._verificar_expressao(node.SecondOperand)
                erros = erros_esq + erros_dir
                op = node.operator.type

                if op in _OPERADORES_COMPARACAO:
                    if tipo_esq and tipo_dir and tipo_esq != tipo_dir:
                        if not (tipo_esq in _TIPOS_NUMERICOS and tipo_dir in _TIPOS_NUMERICOS):
                            erros.append(SemanticError(
                                f"Comparação inválida entre {tipo_esq.value} e {tipo_dir.value}."
                            ))
                    return PrimitiveType.BOOL, erros

                if op in _OPERADORES_LOGICOS:
                    return PrimitiveType.BOOL, erros

                if op in _OPERADORES_ARITMETICOS:
                    for nome, tipo in (('esquerdo', tipo_esq), ('direito', tipo_dir)):
                        if tipo is not None and tipo not in _TIPOS_NUMERICOS:
                            erros.append(SemanticError(
                                f"Operando {nome} da operação aritmética tem tipo incompatível: {tipo.value}."
                            ))
                    tipo_res = None
                    if tipo_esq in _TIPOS_NUMERICOS and tipo_dir in _TIPOS_NUMERICOS:
                        tipo_res = (PrimitiveType.FLOAT
                                    if PrimitiveType.FLOAT in {tipo_esq, tipo_dir}
                                    else PrimitiveType.INTEGER)
                    return tipo_res, erros

                return None, erros

            case MonadicOperation():
                _, erros = self._verificar_expressao(node.operand)
                return PrimitiveType.BOOL, erros

        return None, []

    def _visit_print(self, node: PrintStatement) -> list[SemanticError]:
        return []

    def _visit_return(self, node: ReturnStatement) -> list[SemanticError]:
        return []

    # --- expression evaluators ---

    def _avaliar_expressao_int(self, values: Literal) -> int:
        palavras = [v for v in values if isinstance(v, str)]

        if len(palavras) == 1 and palavras[0].lstrip('-').isdigit():
            return int(palavras[0])

        return int(''.join(str(len(p)) for p in palavras))

    def _avaliar_expressao_float(self, values: Literal) -> float:
        palavras = [v for v in values if isinstance(v, str)]

        if len(palavras) == 1:
            try:
                return float(palavras[0])
            except ValueError:
                pass

        if '...' in palavras:
            idx = palavras.index('...')
            parte_int = palavras[:idx]
            parte_dec = palavras[idx + 1:]
        else:
            parte_int = palavras
            parte_dec = []

        str_int = ''.join(str(len(w)) for w in parte_int) or '0'
        str_dec = ''.join(str(len(w)) for w in parte_dec)

        return float(f'{str_int}.{str_dec}') if str_dec else float(str_int)
