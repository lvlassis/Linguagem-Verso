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


class TestCondicaoSemantica(unittest.TestCase):

    # --- while ---

    def test_while_variavel_nao_declarada_na_condicao(self):
        _, erros = _analisar("enquanto amor igual 0\ngrito paz.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("'amor' não foi declarada" in e.description for e in erros))

    def test_while_variavel_declarada_na_condicao(self):
        _, erros = _analisar("amor é rocha.\nenquanto amor igual 0\ngrito paz.\n")
        self.assertIsNone(erros)

    def test_while_duas_variaveis_uma_nao_declarada(self):
        _, erros = _analisar("amor é rocha.\nenquanto amor igual paz\ngrito amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("'paz' não foi declarada" in e.description for e in erros))

    # --- if: variáveis não declaradas ---

    def test_if_ambas_variaveis_nao_declaradas(self):
        _, erros = _analisar("se amor igual paz então\ngrito amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("'amor' não foi declarada" in e.description for e in erros))

    def test_if_uma_variavel_nao_declarada(self):
        _, erros = _analisar("amor é rocha.\nse amor igual paz então\ngrito amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("'paz' não foi declarada" in e.description for e in erros))

    def test_if_variaveis_declaradas_sem_erro(self):
        _, erros = _analisar("amor é rocha.\npaz é rocha.\nse amor igual paz então\ngrito amor.\n")
        self.assertIsNone(erros)

    def test_if_not_com_variaveis_declaradas(self):
        _, erros = _analisar("amor é rocha.\npaz é rocha.\nse não amor igual paz então\ngrito amor.\n")
        self.assertIsNone(erros)

    def test_if_not_com_variavel_nao_declarada(self):
        _, erros = _analisar("amor é rocha.\nse não amor igual paz então\ngrito amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("'paz' não foi declarada" in e.description for e in erros))

    # --- inferência de tipo em expressões aritméticas ---

    def test_expressao_int_mais_int_valida(self):
        _, erros = _analisar(
            "amor é rocha.\npaz é rocha.\n"
            "se amor acresce paz igual 0 então\ngrito amor.\n"
        )
        self.assertIsNone(erros)

    def test_expressao_int_mais_float_valida(self):
        _, erros = _analisar(
            "amor é rocha.\npaz é bruma.\n"
            "se amor acresce paz igual 0 então\ngrito amor.\n"
        )
        self.assertIsNone(erros)

    def test_expressao_aritmetica_com_string_invalida(self):
        _, erros = _analisar(
            "amor é verso.\npaz é rocha.\n"
            "se amor acresce paz igual 0 então\ngrito amor.\n"
        )
        self.assertIsNotNone(erros)
        self.assertTrue(any("aritmética" in e.description for e in erros))

    def test_expressao_aritmetica_com_bool_invalida(self):
        _, erros = _analisar(
            "amor é dilema.\npaz é rocha.\n"
            "se amor acresce paz igual 0 então\ngrito amor.\n"
        )
        self.assertIsNotNone(erros)
        self.assertTrue(any("aritmética" in e.description for e in erros))

    # --- comparação entre tipos incompatíveis ---

    def test_comparacao_int_com_string_invalida(self):
        _, erros = _analisar(
            "amor é rocha.\npaz é verso.\n"
            "se amor igual paz então\ngrito amor.\n"
        )
        self.assertIsNotNone(erros)
        self.assertTrue(any("Comparação inválida" in e.description for e in erros))

    def test_comparacao_int_com_float_valida(self):
        _, erros = _analisar(
            "amor é rocha.\npaz é bruma.\n"
            "se amor igual paz então\ngrito amor.\n"
        )
        self.assertIsNone(erros)


class TestValidacaoTiposNaoNumericos(unittest.TestCase):

    # --- char ---

    def test_char_declaracao_com_variavel_compativel(self):
        _, erros = _analisar("paz é traço.\nalma é traço paz.\n")
        self.assertIsNone(erros)

    def test_char_declaracao_com_variavel_incompativel(self):
        _, erros = _analisar("amor é rocha.\nalma é traço amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any('incompatível' in e.description for e in erros))

    def test_char_declaracao_com_variavel_nao_declarada(self):
        _, erros = _analisar("alma é traço cor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("'cor' não foi declarada" in e.description for e in erros))

    def test_char_atribuicao_com_variavel_compativel(self):
        _, erros = _analisar("paz é traço.\nalma é traço.\nalma é paz.\n")
        self.assertIsNone(erros)

    def test_char_atribuicao_com_variavel_incompativel(self):
        _, erros = _analisar("amor é rocha.\nalma é traço.\nalma é amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any('incompatível' in e.description for e in erros))

    # --- string ---

    def test_string_declaracao_com_variavel_compativel(self):
        _, erros = _analisar("canto é verso.\npoema é verso canto.\n")
        self.assertIsNone(erros)

    def test_string_declaracao_com_variavel_incompativel(self):
        _, erros = _analisar("amor é rocha.\npoema é verso amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any('incompatível' in e.description for e in erros))

    def test_string_atribuicao_com_variavel_incompativel(self):
        _, erros = _analisar("amor é rocha.\npoema é verso.\npoema é amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any('incompatível' in e.description for e in erros))

    # --- bool ---

    def test_bool_declaracao_com_literal_verdadeiro(self):
        _, erros = _analisar("que viver seja dilema verdadeiro.\n")
        self.assertIsNone(erros)

    def test_bool_declaracao_com_literal_falso(self):
        _, erros = _analisar("que morte seja dilema falso.\n")
        self.assertIsNone(erros)

    def test_bool_declaracao_com_variavel_compativel(self):
        _, erros = _analisar("morte é dilema.\nviver é dilema morte.\n")
        self.assertIsNone(erros)

    def test_bool_declaracao_com_variavel_incompativel(self):
        _, erros = _analisar("amor é rocha.\nviver é dilema amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any('incompatível' in e.description for e in erros))

    def test_bool_atribuicao_com_variavel_compativel(self):
        _, erros = _analisar("morte é dilema.\nviver é dilema.\nviver é morte.\n")
        self.assertIsNone(erros)

    def test_bool_atribuicao_com_variavel_incompativel(self):
        _, erros = _analisar("amor é rocha.\nviver é dilema.\nviver é amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any('incompatível' in e.description for e in erros))


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


class TestArraySemantica(unittest.TestCase):

    def test_array_int_valores_avaliados(self):
        arvore, erros = _analisar("vida é um compêndio rochoso com amor, dor.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].values, [4, 3])

    def test_array_int_tamanho_avaliado(self):
        arvore, erros = _analisar("vida é um compêndio rochoso de amor.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].size, 4)

    def test_array_float_valores_avaliados(self):
        arvore, erros = _analisar("dados é um compêndio enevoado com breve, leve.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].values, [5, 4])

    def test_array_char_vazio_sem_erros(self):
        _, erros = _analisar("letras é um compêndio traçado.\n")
        self.assertIsNone(erros)

    def test_array_redeclaracao_gera_erro(self):
        _, erros = _analisar("vida é um compêndio rochoso.\nvida é um compêndio rochoso.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("já foi declarada" in e.description for e in erros))

    def test_conjunto_alias_sem_erros(self):
        _, erros = _analisar("sons é um conjunto rochoso de eco.\n")
        self.assertIsNone(erros)

    def test_array_bool_dubio_sem_erros(self):
        _, erros = _analisar("bandeiras é um compêndio dúbio.\n")
        self.assertIsNone(erros)

    def test_array_string_versejado_sem_erros(self):
        _, erros = _analisar("poemas é um compêndio versejado.\n")
        self.assertIsNone(erros)

    def test_array_valores_numericos_literais(self):
        # literais numéricos são convertidos para int, não contados por letras
        arvore, erros = _analisar("notas é um compêndio rochoso com 4, 3, 10.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].values, [4, 3, 10])

    def test_array_tamanho_numerico_literal(self):
        arvore, erros = _analisar("notas é um compêndio rochoso de 5.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].size, 5)

    def test_array_rochosa_variante_feminina(self):
        _, erros = _analisar("pedras é um compêndio rochosa.\n")
        self.assertIsNone(erros)

    def test_array_cinzento_tamanho_avaliado(self):
        # sombra=6 letras → int tons[6]
        arvore, erros = _analisar("tons é um compêndio cinzento de sombra.\n")
        self.assertIsNone(erros)
        self.assertEqual(arvore.instructions[0].size, 6)

    def test_array_nao_interfere_com_declaracao_escalar(self):
        _, erros = _analisar("vida é um compêndio rochoso com amor, dor.\nfogo é rocha.\n")
        self.assertIsNone(erros)


class TestScanSemantica(unittest.TestCase):

    def test_scan_variavel_declarada_sem_erros(self):
        _, erros = _analisar("amor é verso.\nescuto amor.\n")
        self.assertIsNone(erros)

    def test_scan_alias_escute_sem_erros(self):
        _, erros = _analisar("amor é verso.\nescute amor.\n")
        self.assertIsNone(erros)

    def test_scan_alias_ouço_sem_erros(self):
        _, erros = _analisar("amor é verso.\nouço amor.\n")
        self.assertIsNone(erros)

    def test_scan_alias_ouça_sem_erros(self):
        _, erros = _analisar("amor é verso.\nouça amor.\n")
        self.assertIsNone(erros)

    def test_scan_com_artigo_sem_erros(self):
        _, erros = _analisar("amor é verso.\nescuto o amor.\n")
        self.assertIsNone(erros)

    def test_scan_variavel_nao_declarada_gera_erro(self):
        _, erros = _analisar("escuto amor.\n")
        self.assertIsNotNone(erros)
        self.assertTrue(any("'amor' não foi declarada" in e.description for e in erros))


if __name__ == '__main__':
    unittest.main()
