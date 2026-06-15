import unittest

from verso.token import tokenize
from verso.sintaxe.parser import Parser
from verso.codigo.gerador import GeradorCodigo


def _compilar(fonte: str) -> str:
    tokens = tokenize(fonte)
    programa = Parser(tokens).parse_program()
    return GeradorCodigo().gerar(programa)


class TestDeclaracaoVariavel(unittest.TestCase):

    def test_int_rocha(self):
        self.assertEqual(_compilar("amor é rocha.\n"), "int amor;")

    def test_float_bruma(self):
        self.assertEqual(_compilar("paz é bruma.\n"), "float paz;")

    def test_float_nevoa(self):
        self.assertEqual(_compilar("paz é névoa.\n"), "float paz;")

    def test_float_cinza(self):
        self.assertEqual(_compilar("paz é cinza.\n"), "float paz;")

    def test_char_suspiro(self):
        self.assertEqual(_compilar("alma é suspiro.\n"), "char alma;")

    def test_char_traco(self):
        self.assertEqual(_compilar("alma é traço.\n"), "char alma;")

    def test_string_verso(self):
        self.assertEqual(_compilar("canto é verso.\n"), "char* canto;")

    def test_string_cancao(self):
        self.assertEqual(_compilar("canto é canção.\n"), "char* canto;")

    def test_string_prosa(self):
        self.assertEqual(_compilar("canto é prosa.\n"), "char* canto;")

    def test_bool_dilema(self):
        self.assertEqual(_compilar("duvida é dilema.\n"), "bool duvida;")

    def test_bool_dualidade(self):
        self.assertEqual(_compilar("duvida é dualidade.\n"), "bool duvida;")

    def test_forma_que_seja(self):
        self.assertEqual(_compilar("que o amor seja rocha.\n"), "int amor;")

    def test_maiuscula_normalizada(self):
        self.assertEqual(_compilar("Amor é rocha.\n"), "int amor;")


class TestAtribuicao(unittest.TestCase):

    def test_atribuicao_variavel(self):
        self.assertEqual(_compilar("amor é paz.\n"), "amor = paz;")


class TestPrograma(unittest.TestCase):

    def test_multiplas_declaracoes(self):
        fonte = "amor é rocha.\npaz é bruma.\n"
        self.assertEqual(_compilar(fonte), "int amor;\nfloat paz;")

    def test_linha_vazia_ignorada(self):
        fonte = "\namor é rocha.\n"
        self.assertEqual(_compilar(fonte), "int amor;")

    def test_declaracao_seguida_de_atribuicao(self):
        fonte = "amor é rocha.\namor é paz.\n"
        self.assertEqual(_compilar(fonte), "int amor;\namor = paz;")


if __name__ == '__main__':
    unittest.main()
