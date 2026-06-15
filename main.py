from verso.semantica.semantica import SemanticAnalyzer
from verso.codigo.gerador import GeradorCodigo
from verso.token import tokenize
from verso.sintaxe.parser import Parser


programa = """amor é rocha.
digo que te amo.
"""

def test_tokenize(codigo):
    tokens = tokenize(codigo)

    print(tokens)


def test_parser(codigo):
    tokens = tokenize(codigo)
    parser = Parser(tokens)
    program = parser.parse_program()

    print(program)

def test_semantic(codigo):
    tokens = tokenize(codigo)
    parser = Parser(tokens)
    arvore_sintatica = parser.parse_program()

    semantic_analizer = SemanticAnalyzer()
    arvore_anotada, erros = semantic_analizer.analyse(arvore_sintatica)
    if erros:
        for e in erros:
            print(e)
        return

    print(arvore_anotada)
        

def test_gerar_codigo(codigo):
    tokens = tokenize(codigo)
    parser = Parser(tokens)
    arvore_sintatica = parser.parse_program()
    semantic_analizer = SemanticAnalyzer()
    programa, erros = semantic_analizer.analyse(arvore_sintatica)
    if erros:
        for e in erros:
            print(e)
        return

    codigo = GeradorCodigo().gerar(programa)

    print(codigo)

test_gerar_codigo(programa)
