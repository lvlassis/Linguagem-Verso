import unittest

from verso.token import tokenize
from verso.sintaxe.parser import Parser
from verso.codigo.gerador import GeradorCodigo


def _compilar(fonte: str) -> str:
    tokens = tokenize(fonte)
    programa = Parser(tokens).parse_program()
    full = GeradorCodigo().gerar(programa)
    # extrai o corpo entre "int main() {" e "return 0;" e desfaz o recuo de 4 espaços
    start = full.index('int main() {\n') + len('int main() {\n')
    end = full.rindex('\nreturn 0;\n}')
    body = full[start:end]
    return '\n'.join(line[4:] if line.startswith('    ') else line for line in body.split('\n'))


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


class TestLiteraisNumericos(unittest.TestCase):

    def test_int_literal_atribuicao(self):
        self.assertEqual(_compilar("amor é 42.\n"), "amor = 42;")

    def test_float_declaracao_com_valor_literal(self):
        self.assertEqual(_compilar("paixao é bruma 3.14.\n"), "float paixao = 3.14;")

    def test_float_literal_atribuicao(self):
        self.assertEqual(_compilar("paixao é 3.14.\n"), "paixao = 3.14;")

    def test_bool_literal_verdadeiro_atribuicao(self):
        self.assertEqual(_compilar("viver é verdadeiro.\n"), "viver = 1;")

    def test_bool_literal_falso_atribuicao(self):
        self.assertEqual(_compilar("viver é falso.\n"), "viver = 0;")


class TestPrint(unittest.TestCase):

    def test_print_grito(self):
        self.assertEqual(_compilar("grito amor.\n"), 'printf("amor\\n");')

    def test_print_gritarei(self):
        self.assertEqual(_compilar("gritarei paz.\n"), 'printf("paz\\n");')

    def test_print_digo_que(self):
        self.assertEqual(_compilar("digo que amor.\n"), 'printf("amor\\n");')

    def test_print_multiplas_palavras(self):
        self.assertEqual(_compilar("grito te amo.\n"), 'printf("te amo\\n");')

    def test_print_sem_argumentos(self):
        self.assertEqual(_compilar("grito.\n"), 'printf("\\n");')

    def test_print_no_while(self):
        fonte = "enquanto verdadeiro\ngrito amor.\n"
        esperado = "while (true) {\n    " + 'printf("amor\\n");' + "\n}"
        self.assertEqual(_compilar(fonte), esperado)


class TestBreakContinueReturn(unittest.TestCase):

    def test_break_no_while(self):
        fonte = "enquanto verdadeiro\ndesista.\n"
        esperado = "while (true) {\n    break;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_break_alias_finde(self):
        fonte = "enquanto verdadeiro\nfinde.\n"
        esperado = "while (true) {\n    break;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_continue_no_while(self):
        fonte = "enquanto verdadeiro\navance.\n"
        esperado = "while (true) {\n    continue;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_continue_alias_prossiga(self):
        fonte = "enquanto verdadeiro\nprossiga.\n"
        esperado = "while (true) {\n    continue;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_return_sem_valor(self):
        self.assertEqual(_compilar("retorne.\n"), "return;")

    def test_return_com_valor(self):
        self.assertEqual(_compilar("retorne amor.\n"), "return amor;")

    def test_return_alias_volte(self):
        self.assertEqual(_compilar("volte.\n"), "return;")

    def test_return_alias_devolva(self):
        self.assertEqual(_compilar("devolva amor.\n"), "return amor;")


class TestIf(unittest.TestCase):

    def test_if_igualdade(self):
        fonte = "se amor igual paz então\ngrito amor.\n"
        esperado = "if (amor == paz) {\n    " + 'printf("amor\\n");' + "\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_if_maior(self):
        fonte = "se amor maior 10 então\ngrito amor.\n"
        esperado = "if (amor > 10) {\n    " + 'printf("amor\\n");' + "\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_if_menor(self):
        fonte = "se amor menor 5 então\ngrito paz.\n"
        esperado = "if (amor < 5) {\n    " + 'printf("paz\\n");' + "\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_if_diferente(self):
        fonte = "se amor diferente paz então\ngrito amor.\n"
        esperado = "if (amor != paz) {\n    " + 'printf("amor\\n");' + "\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_if_com_else(self):
        fonte = "se amor igual paz então\ngrito amor.\nsenão\ngrito paz.\n"
        esperado = (
            "if (amor == paz) {\n    " + 'printf("amor\\n");' + "\n}"
            " else {\n    " + 'printf("paz\\n");' + "\n}"
        )
        self.assertEqual(_compilar(fonte), esperado)

    def test_if_not(self):
        fonte = "se não amor igual paz então\ngrito amor.\n"
        esperado = "if (!(amor == paz)) {\n    " + 'printf("amor\\n");' + "\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_if_corpo_vazio(self):
        fonte = "se amor igual paz então\n.\n"
        self.assertEqual(_compilar(fonte), "if (amor == paz) {\n\n}")

    def test_if_declaracao_no_corpo(self):
        fonte = "se amor igual paz então\nsol é rocha.\n"
        esperado = "if (amor == paz) {\n    int sol;\n}"
        self.assertEqual(_compilar(fonte), esperado)


class TestWhile(unittest.TestCase):

    def test_condicao_igualdade(self):
        fonte = "enquanto amor igual 10\namor é paz.\n"
        esperado = "while (amor == 10) {\n    amor = paz;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_condicao_diferente(self):
        fonte = "enquanto amor diferente paz\namor é sutil.\n"
        esperado = "while (amor != paz) {\n    amor = sutil;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_corpo_multiplas_instrucoes(self):
        fonte = "enquanto amor igual 10\namor é rocha\npaz é bruma.\n"
        esperado = "while (amor == 10) {\n    int amor;\n    float paz;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_condicao_booleano_verdadeiro(self):
        fonte = "enquanto verdadeiro\namor é sutil.\n"
        esperado = "while (true) {\n    amor = sutil;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_condicao_booleano_falso(self):
        fonte = "enquanto falso\namor é sutil.\n"
        esperado = "while (false) {\n    amor = sutil;\n}"
        self.assertEqual(_compilar(fonte), esperado)

    def test_while_precedido_de_declaracao(self):
        fonte = "amor é rocha.\nenquanto amor igual 0\namor é sutil.\n"
        esperado = "int amor;\nwhile (amor == 0) {\n    amor = sutil;\n}"
        self.assertEqual(_compilar(fonte), esperado)


class TestScan(unittest.TestCase):

    def test_escuto(self):
        self.assertEqual(_compilar("escuto amor.\n"), 'scanf("%s", &amor);')

    def test_escute(self):
        self.assertEqual(_compilar("escute amor.\n"), 'scanf("%s", &amor);')

    def test_ouço(self):
        self.assertEqual(_compilar("ouço amor.\n"), 'scanf("%s", &amor);')

    def test_ouça(self):
        self.assertEqual(_compilar("ouça amor.\n"), 'scanf("%s", &amor);')

    def test_escuto_com_artigo(self):
        self.assertEqual(_compilar("escuto o amor.\n"), 'scanf("%s", &amor);')

    def test_ouço_com_artigo(self):
        self.assertEqual(_compilar("ouço o amor.\n"), 'scanf("%s", &amor);')

    def test_scan_apos_declaracao(self):
        fonte = "amor é verso.\nescuto amor.\n"
        esperado = "char* amor;\n" + 'scanf("%s", &amor);'
        self.assertEqual(_compilar(fonte), esperado)

    def test_scan_no_while(self):
        fonte = "amor é verso.\nenquanto verdadeiro\nescuto amor.\n"
        esperado = "char* amor;\nwhile (true) {\n    " + 'scanf("%s", &amor);' + "\n}"
        self.assertEqual(_compilar(fonte), esperado)


if __name__ == '__main__':
    unittest.main()
