from verso.token import tokenize
from verso.sintaxe.parser import Parser


programa = """Se Amor igual rosas então Amor é sutil. # Comentário\n"""

def test_tokenize(codigo):

    tokens = tokenize(codigo)
    print(tokens)

def test_parser(codigo):

    tokens = tokenize(codigo)
    parser = Parser(tokens)
    program = parser.parse_program()

    print(program.instructions)

test_tokenize(programa)
print("")
test_parser(programa)

