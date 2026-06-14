"""
Casos de teste para a função tokenize().

Execute com:  python -m verso.token.test_data
"""

from verso.token import tokenize


def run(name: str, program: str):
    print(f"\n{'─' * 60}")
    print(f"  {name}")
    print(f"  Entrada: {program!r}")
    print()
    try:
        tokens = tokenize(program)
        for tok in tokens:
            print(f"    {tok.type.name:<22} {tok.value!r}")
    except KeyError as e:
        print(f"    ERRO (palavra reservada aponta para TokenType inexistente): {e}")
    except RuntimeError as e:
        print(f"    ERRO léxico: {e}")


# ── Declarações ──────────────────────────────────────────────────────────────

run(
    "Declaração simples (int)",
    "Amor é rocha firme.\n",
)

run(
    "Declaração com artigo",
    "O amor é rocha leve.\n",
)

run(
    "Declaração com 'que … seja'",
    "Que o amor seja rocha amigável.\n",
)

run(
    "Declaração com alias 'és'",
    "Tu és rocha polida.\n",
)

run(
    "Declaração float (bruma)",
    "Paixão é bruma suave.\n",
)

# ── Valores literais ──────────────────────────────────────────────────────────

run(
    "Número inteiro",
    "Amor é 42.\n",
)

run(
    "Número float",
    "Amor é 3.14.\n",
)

run(
    "Literal booleano verdadeiro",
    "Viver é verdadeiro.\n",
)

run(
    "Literal booleano falso",
    "Amar é falso.\n",
)

run(
    "Reticências (ellipse)",
    "Amor é bruma...\n",
)

# ── Comentários ───────────────────────────────────────────────────────────────

run(
    "Comentário inline (deve ser ignorado)",
    "Amor é rocha. # int amor;\n",
)

run(
    "Linha só com comentário",
    "# Esta linha não gera tokens\n",
)

# ── Estruturas de dados ───────────────────────────────────────────────────────

run(
    "Array (compêndio)",
    "A história é um compêndio rochoso.\n",
)

run(
    "Array (coro)",
    "O coral é um coro melodioso.\n",
)

# ── Operadores de comparação ──────────────────────────────────────────────────

run(
    "Comparação: igual",
    "amor igual ódio\n",
)

run(
    "Comparação: como (alias de igual)",
    "amor como ódio\n",
)

run(
    "Comparação: diferente",
    "amor diferente ódio\n",
)

run(
    "Comparação: maior",
    "amor maior ódio\n",
)

run(
    "Comparação: menor",
    "amor menor ódio\n",
)

run(
    "Comparação: até (menor ou igual)",
    "amor até 10\n",
)

# ── Operadores lógicos ────────────────────────────────────────────────────────

run(
    "Operadores: e / ou",
    "amor e ódio ou paz\n",
)

run(
    "Negação: não",
    "não amor\n",
)

# ── Fluxo de controle ─────────────────────────────────────────────────────────

run(
    "Se (if) — keyword é case-sensitive: 'Se' com S maiúsculo",
    "Se o amor não for forte\n",
)

run(
    "Se com s minúsculo — funciona igual após o lower()",
    "se o amor não for forte\n",
)

run(
    "Senão (else)",
    "Senão\n",
)

run(
    "Enquanto (while)",
    "Enquanto o amor durar\n",
)

run(
    "Sendo (for)",
    "Sendo o amor eterno\n",
)

# ── Múltiplas linhas ──────────────────────────────────────────────────────────

run(
    "Duas declarações (EOL separa as linhas)",
    "Amor é rocha.\nPaixão é bruma.\n",
)

# ── Tipos antes com typo no JSON ─────────────────────────────────────────────

run(
    "Declaração com cinza (float)",
    "Paixão é cinza.\n",
)

run(
    "Comparação: distinto (alias de diferente)",
    "amor distinto ódio\n",
)

# ── Controle de fluxo: return / break / continue ──────────────────────────────

run(
    "Return (retorne)",
    "retorne amor\n",
)

run(
    "Break (desista)",
    "desista\n",
)

run(
    "Continue (avance)",
    "avance\n",
)

# ── Maior ou igual (me) ───────────────────────────────────────────────────────

run(
    "Comparação: me (maior ou igual)",
    "amor me ódio\n",
)

# ── Saída ─────────────────────────────────────────────────────────────────────

run(
    "Print: gritarei",
    "gritarei meu amor\n",
)

run(
    "Print: digo que (multi-palavra → token único)",
    "digo que nunca te abandonarei\n",
)

# ── Blocos condicionais ───────────────────────────────────────────────────────
#
# Observação: 'for' (verbo português) não está nas constantes → vira VARIABLE

run(
    "if simples — se o amor for maior que a dor então",
    "se o amor for maior que a dor então\ndigo que tu és digno.\n",
)

run(
    "if com igualdade — se a paz for como o silêncio então",
    "se a paz for como o silêncio então\ndigo que és belo.\n",
)

run(
    "if com negação — se o amor não for forte então",
    "se o amor não for forte então\ndesista.\n",
)

run(
    "if-else — se / senão",
    "se o amor for maior que a dor então\ndigo que és digno.\nsenão\ndigo que és pó.\n",
)

run(
    "if-else encadeado com bloco fechado por ponto",
    "se o amor for maior que a dor então\ndigo que és digno.\nsenão\ndesista.\n",
)
