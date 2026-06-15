import sys
from pathlib import Path

from verso.token import tokenize
from verso.sintaxe.parser import Parser
from verso.semantica.semantica import SemanticAnalyzer
from verso.codigo.gerador import GeradorCodigo


def compilar(fonte: str) -> str:
    tokens = tokenize(fonte)
    arvore = Parser(tokens).parse_program()

    arvore, erros = SemanticAnalyzer().analyse(arvore)
    if erros:
        for e in erros:
            print(f"[erro semântico] {e.description}", file=sys.stderr)
        return ""

    return GeradorCodigo().gerar(arvore)


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.vs>", file=sys.stderr)
        sys.exit(1)

    caminho = Path(sys.argv[1])
    if not caminho.exists():
        print(f"[verso] erro: '{caminho}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    codigo = compilar(caminho.read_text(encoding='utf-8'))
    if not codigo:
        sys.exit(1)

    saida = caminho.parent.parent / "bin" / caminho.with_suffix('.c').name
    saida.write_text(codigo, encoding='utf-8')
    print(f"[verso] compilado → {saida}")


if __name__ == "__main__":
    main()
