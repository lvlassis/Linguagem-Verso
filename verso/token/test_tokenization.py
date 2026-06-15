import unittest

from verso.token import tokenize, Token, TokenType, PrimitiveType


class TestDeclaracao(unittest.TestCase):

    def test_declaracao_simples(self):
        tokens = tokenize("Amor é rocha.\n")
        self.assertEqual(tokens[0], Token(TokenType.VARIABLE, 'amor'))
        self.assertEqual(tokens[1], Token(TokenType.DECL_ATTR, 'é'))
        self.assertEqual(tokens[2], Token(TokenType.PRIMITIVE_TYPE, PrimitiveType.INTEGER))
        self.assertEqual(tokens[3], Token(TokenType.DOT, '.'))
        self.assertEqual(tokens[4], Token(TokenType.EOL, '\n'))

    def test_declaracao_com_artigo(self):
        tokens = tokenize("O amor é rocha.\n")
        self.assertEqual(tokens[0], Token(TokenType.ARTICLE, 'o'))
        self.assertEqual(tokens[1], Token(TokenType.VARIABLE, 'amor'))

    def test_declaracao_que_seja(self):
        tokens = tokenize("Que o amor seja rocha.\n")
        self.assertEqual(tokens[0], Token(TokenType.CONJUNCTION, 'que'))
        self.assertEqual(tokens[3], Token(TokenType.DECL_ATTR, 'seja'))

    def test_aliases_de_declaracao(self):
        for alias in ('guarda', 'encerra', 'guarde', 'encerre'):
            with self.subTest(alias=alias):
                tokens = tokenize(f"amor {alias} paz.\n")
                self.assertEqual(tokens[1].type, TokenType.DECL_ATTR)

    def test_comentario_descartado(self):
        tokens = tokenize("# int amor;\n")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, TokenType.EOL)


class TestTiposPrimitivos(unittest.TestCase):

    def _tipo(self, program: str) -> Token:
        return next(t for t in tokenize(program) if t.type == TokenType.PRIMITIVE_TYPE)

    def test_int_rocha(self):
        self.assertEqual(self._tipo("vida é rocha.\n").value, PrimitiveType.INTEGER)

    def test_float_bruma(self):
        self.assertEqual(self._tipo("paixão é bruma.\n").value, PrimitiveType.FLOAT)

    def test_float_nevoa(self):
        self.assertEqual(self._tipo("paixão é névoa.\n").value, PrimitiveType.FLOAT)

    def test_float_cinza(self):
        self.assertEqual(self._tipo("paixão é cinza.\n").value, PrimitiveType.FLOAT)

    def test_char_suspiro(self):
        self.assertEqual(self._tipo("a vida é um suspiro.\n").value, PrimitiveType.CHAR)

    def test_char_traco(self):
        self.assertEqual(self._tipo("a vida é um traço.\n").value, PrimitiveType.CHAR)

    def test_string_verso(self):
        self.assertEqual(self._tipo("que o amor seja um verso.\n").value, PrimitiveType.STRING)

    def test_string_cancao(self):
        self.assertEqual(self._tipo("que o amor seja uma canção.\n").value, PrimitiveType.STRING)

    def test_bool_dilema(self):
        self.assertEqual(self._tipo("viver é um dilema.\n").value, PrimitiveType.BOOL)

    def test_bool_dualidade(self):
        self.assertEqual(self._tipo("viver é uma dualidade.\n").value, PrimitiveType.BOOL)


class TestLiterais(unittest.TestCase):

    def test_numero_inteiro(self):
        tokens = tokenize("amor é 42.\n")
        self.assertEqual(tokens[2], Token(TokenType.NUMBER, '42'))

    def test_numero_float(self):
        tokens = tokenize("amor é 3.14.\n")
        self.assertEqual(tokens[2], Token(TokenType.NUMBER, '3.14'))

    def test_booleano_verdadeiro(self):
        tokens = tokenize("viver é verdadeiro.\n")
        self.assertEqual(tokens[2].type, TokenType.BOOLEAN_TRUE)

    def test_booleano_falso(self):
        tokens = tokenize("amar é falso.\n")
        self.assertEqual(tokens[2].type, TokenType.BOOLEAN_FALSE)

    def test_ellipse(self):
        tokens = tokenize("amor é bruma...\n")
        self.assertIn(Token(TokenType.ELLIPSE, '...'), tokens)


class TestOperadoresComparacao(unittest.TestCase):

    def _op(self, program: str) -> TokenType:
        return tokenize(program)[1].type

    def test_igual(self):
        self.assertEqual(self._op("amor igual ódio\n"), TokenType.EQUAL)

    def test_como(self):
        self.assertEqual(self._op("amor como ódio\n"), TokenType.EQUAL)

    def test_diferente(self):
        self.assertEqual(self._op("amor diferente ódio\n"), TokenType.DIFFERENT)

    def test_distinto(self):
        self.assertEqual(self._op("amor distinto ódio\n"), TokenType.DIFFERENT)

    def test_maior(self):
        self.assertEqual(self._op("amor maior ódio\n"), TokenType.GREATER_THAN)

    def test_menor(self):
        self.assertEqual(self._op("amor menor ódio\n"), TokenType.LESS_THAN)

    def test_ate(self):
        self.assertEqual(self._op("amor até 10\n"), TokenType.LESS_OR_EQUAL)

    def test_me(self):
        self.assertEqual(self._op("amor me ódio\n"), TokenType.GREATER_OR_EQUAL)


class TestOperadoresLogicos(unittest.TestCase):

    def test_e(self):
        self.assertEqual(tokenize("amor e ódio\n")[1].type, TokenType.AND)

    def test_ou(self):
        self.assertEqual(tokenize("amor ou ódio\n")[1].type, TokenType.OR)

    def test_nao(self):
        self.assertEqual(tokenize("não amor\n")[0].type, TokenType.NOT)


class TestFluxoDeControle(unittest.TestCase):

    def test_se(self):
        tokens = tokenize("se o amor não for forte então\n")
        self.assertEqual(tokens[0].type, TokenType.IF)
        self.assertEqual(tokens[-2].type, TokenType.THEN)

    def test_senao(self):
        self.assertEqual(tokenize("senão\n")[0].type, TokenType.ELSE)

    def test_enquanto(self):
        self.assertEqual(tokenize("enquanto o amor durar\n")[0].type, TokenType.WHILE)

    def test_sendo(self):
        self.assertEqual(tokenize("sendo o amor eterno\n")[0].type, TokenType.FOR)

    def test_case_insensitive(self):
        self.assertEqual(tokenize("Se o amor durar então\n")[0].type, TokenType.IF)
        self.assertEqual(tokenize("Enquanto o amor durar\n")[0].type, TokenType.WHILE)


class TestSaida(unittest.TestCase):

    def test_grito(self):
        tokens = tokenize("grito amor\n")
        self.assertEqual(tokens[0].type, TokenType.PRINT)
        self.assertEqual(tokens[0].value, 'grito')

    def test_gritarei(self):
        tokens = tokenize("gritarei amor\n")
        self.assertEqual(tokens[0].type, TokenType.PRINT)
        self.assertEqual(tokens[0].value, 'gritarei')

    def test_digo_que(self):
        tokens = tokenize("digo que amor\n")
        self.assertEqual(tokens[0].type, TokenType.PRINT)
        self.assertEqual(tokens[0].value, 'digo que')

    def test_digo_que_emite_token_unico(self):
        # "digo que" deve virar 1 token, não 2
        tokens = tokenize("digo que amor\n")
        self.assertNotEqual(tokens[1].type, TokenType.CONJUNCTION)


class TestDesvios(unittest.TestCase):

    def _tipo(self, program: str) -> TokenType:
        return tokenize(program)[0].type

    def test_return_retorne(self):
        self.assertEqual(self._tipo("retorne amor\n"), TokenType.RETURN)

    def test_return_volte(self):
        self.assertEqual(self._tipo("volte amor\n"), TokenType.RETURN)

    def test_break_desista(self):
        self.assertEqual(self._tipo("desista\n"), TokenType.BREAK)

    def test_break_finde(self):
        self.assertEqual(self._tipo("finde\n"), TokenType.BREAK)


class TestEntrada(unittest.TestCase):

    def _tipo(self, program: str) -> TokenType:
        return tokenize(program)[0].type

    def test_escuto(self):
        tokens = tokenize("escuto amor\n")
        self.assertEqual(tokens[0].type, TokenType.SCAN)

    def test_escute(self):
        tokens = tokenize("escute amor\n")
        self.assertEqual(tokens[0].type, TokenType.SCAN)

    def test_ouço(self):
        tokens = tokenize("ouço amor\n")
        self.assertEqual(tokens[0].type, TokenType.SCAN)

    def test_ouça(self):
        tokens = tokenize("ouça amor\n")
        self.assertEqual(tokens[0].type, TokenType.SCAN)

    def test_escuto_com_artigo_emite_token_unico(self):
        # "escuto o" deve virar 1 token SCAN, não SCAN + ARTICLE
        tokens = tokenize("escuto o amor\n")
        self.assertEqual(tokens[0].type, TokenType.SCAN)
        self.assertEqual(tokens[1].type, TokenType.VARIABLE)

    def test_ouço_com_artigo_emite_token_unico(self):
        tokens = tokenize("ouço o amor\n")
        self.assertEqual(tokens[0].type, TokenType.SCAN)
        self.assertEqual(tokens[1].type, TokenType.VARIABLE)

    def test_continue_avance(self):
        self.assertEqual(self._tipo("avance\n"), TokenType.CONTINUE)

    def test_continue_prossiga(self):
        self.assertEqual(self._tipo("prossiga\n"), TokenType.CONTINUE)


if __name__ == '__main__':
    unittest.main()
