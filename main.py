from verso.tokens import tokenize

def test_tokenize():
    programa = """amor é rocha que quando quebra doi no peito. """
    programa = """Amor é pacto ... sagrado. Amor é 10.asdf00 # Comentário\n"""

    tokens = tokenize(programa)
    print(tokens)


test_tokenize()

