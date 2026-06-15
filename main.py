from verso.token import tokenize
from verso.sintaxe.parser import Parser
from verso.semantica.semantica import SemanticAnalyzer
from verso.codigo.gerador import GeradorCodigo


programa = """\
# ── tipos básicos ────────────────────────────────
amor é rocha.
paz é bruma.
vida é dilema.
alma é traço.
canto é verso.

# ── expressões poéticas na declaração ───────────
# "dura"(4) + "demais"(6)  →  int peso = 46
que o peso seja rocha dura demais.
# "eterna"(6) ... "suave"(5)  →  float leveza = 6.5
que a leveza seja bruma eterna... suave.

# ── atribuições com literais ─────────────────────
amor é 42.
paz é 3.14.
vida é verdadeiro.

# ── saída (três formas) ──────────────────────────
grito amor.
gritarei leveza.
digo que hello world.

# ── condicional ──────────────────────────────────
se amor maior 10 então
grito muito.
senão
grito pouco.

# ── laço com desvio de fluxo ─────────────────────
# '.' standalone fecha o if; 'grito amor.' fecha o while
enquanto vida
se amor igual 0 então
desista
.
grito amor.

# ── retorno ──────────────────────────────────────
retorne amor.
"""


def compilar(fonte: str) -> str:
    tokens = tokenize(fonte)
    arvore = Parser(tokens).parse_program()

    arvore, erros = SemanticAnalyzer().analyse(arvore)
    if erros:
        for e in erros:
            print(f"[erro semântico] {e.description}")
        return ""

    return GeradorCodigo().gerar(arvore)


if __name__ == "__main__":
    resultado = compilar(programa)
    if resultado:
        print(resultado)
