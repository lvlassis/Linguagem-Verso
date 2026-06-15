from verso.semantica.semantica import SemanticAnalyzer
from verso.token import tokenize
from verso.sintaxe.parser import Parser


programa = """Amor é rocha. Amor é sutil # Comentário\n"""

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
        


test_semantic(programa)

