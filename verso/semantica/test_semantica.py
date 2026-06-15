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

    def test_float_avalia_contagem_letras(self):
        # "eterna"(6) → 6.0
        arvore, erros = _analisar("paixao é bruma eterna.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [6.0])


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


class TestExpressaoFloat(unittest.TestCase):

    def test_float_declaracao_com_reticencias(self):
        # "eterna"(6) ... "suave"(5) → 6.5
        arvore, erros = _analisar("paixao é bruma eterna... suave.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [6.5])

    def test_float_declaracao_multiplas_palavras_em_cada_parte(self):
        # "dura"(4) + "demais"(6) ... "muito"(5) + "mesmo"(5) → 46.55
        arvore, erros = _analisar("paixao é bruma dura demais... muito mesmo.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [46.55])

    def test_float_declaracao_sem_reticencias(self):
        # "eterna"(6) → 6.0  (sem parte decimal)
        arvore, erros = _analisar("paixao é bruma eterna.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [6.0])

    def test_float_declaracao_nevoa(self):
        # mesmo comportamento com alias névoa
        arvore, erros = _analisar("paixao é névoa eterna.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [6.0])

    def test_float_declaracao_literal(self):
        arvore, erros = _analisar("paixao é bruma 3.14.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [3.14])

    def test_float_atribuicao_palavra(self):
        # "eterna"(6) → 6.0
        arvore, erros = _analisar("paixao é bruma.\npaixao é eterna.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[1].value, [6.0])

    def test_float_atribuicao_com_reticencias(self):
        # "eterna"(6) ... "suave"(5) → 6.5
        arvore, erros = _analisar("paixao é bruma.\npaixao é eterna... suave.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[1].value, [6.5])

    def test_float_atribuicao_literal(self):
        arvore, erros = _analisar("paixao é bruma.\npaixao é 3.14.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[1].value, ['3.14'])


class TestLiteralNumericoInt(unittest.TestCase):

    def test_literal_int_declaracao(self):
        arvore, erros = _analisar("amor é rocha 42.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].value, [42])

    def test_literal_int_atribuicao(self):
        arvore, erros = _analisar("amor é rocha.\namor é 42.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[1].value, ['42'])


class TestEscopoBloco(unittest.TestCase):

    def test_variavel_interna_nao_vaza_do_while(self):
        # amor declarado dentro do while não pode ser usado fora
        fonte = "amor é rocha.\nenquanto verdadeiro\npaz é bruma.\namor é sutil.\npaz é suave.\n"
        _, erros = _analisar(fonte)
        self.assertIsNotNone(erros)
        self.assertTrue(any("'paz' não foi declarada" in e.description for e in erros))

    def test_variavel_externa_acessivel_dentro_do_while(self):
        _, erros = _analisar("amor é rocha.\nenquanto verdadeiro\namor é sutil.\n")
        self.assertIsNone(erros)

    def test_sombreamento_de_variavel_no_while(self):
        # inner scope pode declarar mesma variável que outer scope (shadowing)
        fonte = "amor é rocha.\nenquanto verdadeiro\namor é bruma.\namor é eterna.\n"
        _, erros = _analisar(fonte)
        self.assertIsNone(erros)

    def test_redeclaracao_no_mesmo_escopo_proibida(self):
        _, erros = _analisar("amor é rocha.\namor é bruma.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("'amor' já foi declarada" in e.description for e in erros))


class TestPrintSemantica(unittest.TestCase):

    def test_print_valido_sem_erros(self):
        _, erros = _analisar("grito amor.\n")
        self.assertIsNone(erros)

    def test_print_multiplas_palavras_sem_erros(self):
        _, erros = _analisar("grito te amo.\n")
        self.assertIsNone(erros)

    def test_print_digo_que_sem_erros(self):
        _, erros = _analisar("digo que paz.\n")
        self.assertIsNone(erros)

    def test_print_com_variavel_declarada_sem_erros(self):
        _, erros = _analisar("amor é rocha.\ngrito amor.\n")
        self.assertIsNone(erros)


class TestBreakContinueReturnSemantica(unittest.TestCase):

    def test_break_sem_erros(self):
        _, erros = _analisar("enquanto verdadeiro\ndesista.\n")
        self.assertIsNone(erros)

    def test_break_alias_finde_sem_erros(self):
        _, erros = _analisar("enquanto verdadeiro\nfinde.\n")
        self.assertIsNone(erros)

    def test_continue_sem_erros(self):
        _, erros = _analisar("enquanto verdadeiro\navance.\n")
        self.assertIsNone(erros)

    def test_return_sem_valor_sem_erros(self):
        _, erros = _analisar("retorne.\n")
        self.assertIsNone(erros)

    def test_return_com_valor_sem_erros(self):
        _, erros = _analisar("amor é rocha.\nretorne amor.\n")
        self.assertIsNone(erros)


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
