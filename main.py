from verso.token import tokenize
from verso.sintaxe.parser import Parser
from verso.semantica.semantica import SemanticAnalyzer
from verso.codigo.gerador import GeradorCodigo


programa = """\
amor é rocha 42
paz é bruma eterna... suave
se amor igual 42 então
grito amor.
senão
grito paz.
"""


def compilar(fonte: str) -> str:
    tokens = tokenize(fonte)
    arvore = Parser(tokens).parse_program()

    arvore, erros = SemanticAnalyzer().analyse(arvore)
    if erros:
        for e in erros:
            print(f"[erro semântico] {e.description}")
        return ""

    return GeradorCodigo().gerar(arvore)


if __name__ == "__main__":
    resultado = compilar(programa)
    if resultado:
        print(resultado)
