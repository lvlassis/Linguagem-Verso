from verso.ast import Program, Statement, VariableDeclaration, Attribution
from verso.token.constants import PrimitiveType

_C_TYPES: dict[PrimitiveType, str] = {
    PrimitiveType.INTEGER: 'int',
    PrimitiveType.FLOAT:   'float',
    PrimitiveType.CHAR:    'char',
    PrimitiveType.STRING:  'char*',
    PrimitiveType.BOOL:    'bool',
}


class GeradorCodigo:
    def gerar(self, program: Program) -> str:
        return '\n'.join(self._visitar(s) for s in program.instructions)

    def _visitar(self, node: Statement) -> str:
        match node:
            case VariableDeclaration():
                return self._gerar_declaracao(node)
            case Attribution():
                return self._gerar_atribuicao(node)
        raise NotImplementedError(f"Geração não implementada para {type(node).__name__}")

    def _gerar_declaracao(self, node: VariableDeclaration) -> str:
        c_type = _C_TYPES[node.varType]
        if node.value:
            return f'{c_type} {node.name} = {" ".join(str(v) for v in node.value)};'
        return f'{c_type} {node.name};'

    def _gerar_atribuicao(self, node: Attribution) -> str:
        return f'{node.name} = {" ".join(str(v) for v in node.value)};'

