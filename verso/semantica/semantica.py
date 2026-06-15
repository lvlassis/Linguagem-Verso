from verso.semantica.constants import SemanticError
from verso.ast import Program, Statement, VariableDeclaration, Attribution
from verso.token.constants import PrimitiveType


class SemanticAnalyzer:
    def __init__(self) -> None:
        self._symbols: dict[str, PrimitiveType] = {}

    def analyse(self, tree: Program) -> tuple[Program, list[SemanticError] | None]:
        errors = []
        for instruction in tree.instructions:
            errors += self._visit(instruction)
        return tree, errors or None

    def _visit(self, node: Statement) -> list[SemanticError]:
        match node:
            case VariableDeclaration():
                return self._visit_declaration(node)
            case Attribution():
                return self._visit_attribution(node)
        return []

    def _visit_declaration(self, node: VariableDeclaration) -> list[SemanticError]:
        if node.name in self._symbols:
            return [SemanticError(f"'{node.name}' já foi declarada.")]
        self._symbols[node.name] = node.varType

        if node.value and node.varType == PrimitiveType.INTEGER:
            node.value = [self._avaliar_expressao_int(node.value)]

        return []

    def _visit_attribution(self, node: Attribution) -> list[SemanticError]:
        errors = []

        if node.name not in self._symbols:
            errors.append(SemanticError(f"'{node.name}' não foi declarada."))
            return errors

        declared_type = self._symbols[node.name]
        palavras = [v for v in node.value if isinstance(v, str)]
        todas_declaradas = all(p in self._symbols for p in palavras)

        if not todas_declaradas and declared_type == PrimitiveType.INTEGER:
            node.value = [self._avaliar_expressao_int(node.value)]
            return []

        for val in palavras:
            if val not in self._symbols:
                errors.append(SemanticError(f"'{val}' não foi declarada."))
            elif self._symbols[val] != declared_type:
                errors.append(SemanticError(
                    f"Tipo incompatível: '{val}' é {self._symbols[val].value}, "
                    f"mas '{node.name}' espera {declared_type.value}."
                ))

        return errors

    def _avaliar_expressao_int(self, values: list) -> int:
        palavras = [v for v in values if isinstance(v, str)]

        if len(palavras) == 1 and palavras[0].lstrip('-').isdigit():
            return int(palavras[0])

        return int(''.join(str(len(p)) for p in palavras))
