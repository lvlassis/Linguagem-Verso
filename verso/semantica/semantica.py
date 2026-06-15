from verso.semantica.constants import SemanticError
from verso.ast import (
    Program, Statement,
    VariableDeclaration, Attribution, WhileLoop, IfBody,
    PrintStatement, BreakStatement, ContinueStatement, ReturnStatement,
)
from verso.token.constants import PrimitiveType


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

        return []

    def _visit_attribution(self, node: Attribution) -> list[SemanticError]:
        if not self._is_declared(node.name):
            return [SemanticError(f"'{node.name}' não foi declarada.")]

        declared_type = self._lookup(node.name)
        palavras = [v for v in node.value if isinstance(v, str)]

        variaveis  = [p for p in palavras if self._is_declared(p)]
        literais   = [p for p in palavras if not self._is_declared(p) and self._is_numeric_literal(p)]
        expressoes = [p for p in palavras if not self._is_declared(p) and not self._is_numeric_literal(p)]

        if expressoes:
            if declared_type == PrimitiveType.INTEGER:
                node.value = [self._avaliar_expressao_int(node.value)]
                return []
            elif declared_type == PrimitiveType.FLOAT:
                node.value = [self._avaliar_expressao_float(node.value)]
                return []
            else:
                return [SemanticError(f"'{expressoes[0]}' não foi declarada.")]

        errors = []
        for val in variaveis:
            val_type = self._lookup(val)
            if val_type != declared_type:
                errors.append(SemanticError(
                    f"Tipo incompatível: '{val}' é {val_type.value}, "
                    f"mas '{node.name}' espera {declared_type.value}."
                ))
        return errors

    def _visit_if(self, node: IfBody) -> list[SemanticError]:
        self._push_scope()
        errors = []
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
        self._push_scope()
        errors = []
        for stmt in node.body:
            errors += self._visit(stmt)
        self._pop_scope()
        return errors

    def _visit_print(self, node: PrintStatement) -> list[SemanticError]:
        return []

    def _visit_return(self, node: ReturnStatement) -> list[SemanticError]:
        return []

    # --- expression evaluators ---

    def _avaliar_expressao_int(self, values: list) -> int:
        palavras = [v for v in values if isinstance(v, str)]

        if len(palavras) == 1 and palavras[0].lstrip('-').isdigit():
            return int(palavras[0])

        return int(''.join(str(len(p)) for p in palavras))

    def _avaliar_expressao_float(self, values: list) -> float:
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
