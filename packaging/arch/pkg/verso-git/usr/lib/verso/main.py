import argparse
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
    parser = argparse.ArgumentParser(
        prog="verso",
        description="Compilador da linguagem Romântica → C",
    )
    parser.add_argument("arquivo", help="arquivo fonte .vs")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--preview",
        action="store_true",
        help="exibe o código C gerado sem criar arquivo",
    )
    group.add_argument(
        "--build",
        action="store_true",
        help="compila e salva o arquivo C em bin/ (padrão)",
    )
    args = parser.parse_args()

    caminho = Path(args.arquivo)
    if not caminho.exists():
        print(f"[verso] erro: '{caminho}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    codigo = compilar(caminho.read_text(encoding='utf-8'))
    if not codigo:
        sys.exit(1)

    if args.preview:
        print(codigo)
        return

    saida = caminho.parent.parent / "bin" / caminho.with_suffix('.c').name
    saida.write_text(codigo, encoding='utf-8')
    print(f"[verso] compilado → {saida}")


if __name__ == "__main__":
    main()
