import unittest

from verso.token import tokenize
from verso.sintaxe.parser import Parser
from verso.semantica.semantica import SemanticAnalyzer


def _analisar(fonte: str):
    tokens = tokenize(fonte)
    programa = Parser(tokens).parse_program()
    return SemanticAnalyzer().analyse(programa)


class TestExpressaoNumerica(unittest.TestCase):

    def test_duas_palavras(self):
        # "dura"(4) + "demais"(6) → 46
        arvore, erros = _analisar("amor é rocha dura demais.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [46])

    def test_uma_palavra(self):
        # "eterna"(6) → 6
        arvore, erros = _analisar("vida é rocha eterna.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [6])

    def test_tres_palavras(self):
        # "muito"(5) + "dura"(4) + "mesmo"(5) → 545
        arvore, erros = _analisar("vida é rocha muito dura mesmo.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [545])

    def test_sem_valor_nao_avalia(self):
        arvore, erros = _analisar("amor é rocha.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [])

    def test_tipo_nao_inteiro_nao_avalia(self):
        # Float: valor permanece como lista de palavras (não avaliado ainda)
        arvore, erros = _analisar("paixao é bruma eterna.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, ['eterna'])


class TestAtribuicaoExpressaoNumerica(unittest.TestCase):

    def test_palavra_unica(self):
        # "sutil"(5) → amor = 5
        arvore, erros = _analisar("amor é rocha.\namor é sutil.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[1].value, [5])

    def test_multiplas_palavras(self):
        # "dura"(4) + "demais"(6) → amor = 46
        arvore, erros = _analisar("amor é rocha.\namor é dura demais.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[1].value, [46])

    def test_variavel_declarada_nao_avalia(self):
        # paz é variável conhecida, deve manter referência
        arvore, erros = _analisar("amor é rocha.\npaz é rocha.\namor é paz.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[2].value, ['paz'])


class TestTabelaDeSimbolos(unittest.TestCase):

    def test_redeclaracao(self):
        _, erros = _analisar("amor é rocha.\namor é rocha.\n")
        self.assertIsNotNone(erros)
        self.assertEqual(len(erros), 1)
        self.assertIn('amor', erros[0].description)

    def test_uso_antes_de_declarar(self):
        _, erros = _analisar("amor é paz.\n")
        self.assertIsNotNone(erros)
        self.assertIn('amor', erros[0].description)

    def test_tipo_incompativel(self):
        _, erros = _analisar("amor é rocha.\npaz é bruma.\namor é paz.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any('incompatível' in e.description for e in erros))

    def test_programa_valido_sem_erros(self):
        _, erros = _analisar("amor é rocha.\npaz é rocha.\namor é paz.\n")
        self.assertIsNone(erros)


if __name__ == '__main__':
    unittest.main()
