from verso.ast import (
    Program, Statement,
    VariableDeclaration, Attribution, WhileLoop,
    PrintStatement, BreakStatement, ContinueStatement, ReturnStatement,
)
from verso.token.constants import Token, TokenType, PrimitiveType

_C_TYPES: dict[PrimitiveType, str] = {
    PrimitiveType.INTEGER: 'int',
    PrimitiveType.FLOAT:   'float',
    PrimitiveType.CHAR:    'char',
    PrimitiveType.STRING:  'char*',
    PrimitiveType.BOOL:    'bool',
}

_C_COMPARISONS: dict[TokenType, str] = {
    TokenType.EQUAL:            '==',
    TokenType.DIFFERENT:        '!=',
    TokenType.GREATER_THAN:     '>',
    TokenType.LESS_THAN:        '<',
    TokenType.GREATER_OR_EQUAL: '>=',
    TokenType.LESS_OR_EQUAL:    '<=',
    TokenType.AND:              '&&',
    TokenType.OR:               '||',
    TokenType.NOT:              '!',
}

_C_BOOLEANS: dict[TokenType, str] = {
    TokenType.BOOLEAN_TRUE:  'true',
    TokenType.BOOLEAN_FALSE: 'false',
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
            case WhileLoop():
                return self._gerar_while(node)
            case PrintStatement():
                return self._gerar_print(node)
            case BreakStatement():
                return 'break;'
            case ContinueStatement():
                return 'continue;'
            case ReturnStatement():
                return self._gerar_return(node)
        raise NotImplementedError(f"Geração não implementada para {type(node).__name__}")

    def _gerar_declaracao(self, node: VariableDeclaration) -> str:
        c_type = _C_TYPES[node.varType]
        if node.value:
            return f'{c_type} {node.name} = {" ".join(str(v) for v in node.value)};'
        return f'{c_type} {node.name};'

    def _gerar_atribuicao(self, node: Attribution) -> str:
        return f'{node.name} = {" ".join(str(v) for v in node.value)};'

    def _gerar_while(self, node: WhileLoop) -> str:
        cond = self._gerar_condicao(node.condition)
        corpo = '\n'.join(f'    {self._visitar(s)}' for s in node.body)
        return f'while ({cond}) {{\n{corpo}\n}}'

    def _gerar_print(self, node: PrintStatement) -> str:
        args = [str(v) for v in node.args if v is not None]
        return f'printf("{" ".join(args)}\\n");'

    def _gerar_return(self, node: ReturnStatement) -> str:
        if node.value:
            vals = ' '.join(str(v) for v in node.value if v is not None)
            return f'return {vals};'
        return 'return;'

    def _gerar_condicao(self, tokens: list[Token]) -> str:
        parts = []
        for t in tokens:
            if t.type in _C_COMPARISONS:
                parts.append(_C_COMPARISONS[t.type])
            elif t.type in _C_BOOLEANS:
                parts.append(_C_BOOLEANS[t.type])
            elif t.value is not None:
                parts.append(str(t.value))
        return ' '.join(parts)
