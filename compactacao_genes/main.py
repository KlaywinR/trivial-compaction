import argparse
import sys
from pathlib import Path

from compactacao import GeneComprimido, ler_sequencia
from compactacao.relatorio import analisar, exercicios_do_pdf, formatar

RAIZ = Path(__file__).resolve().parent
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "saida"


def cmd_exercicios(_args) -> int:
    print(exercicios_do_pdf())
    return 0


def cmd_demo(_args) -> int:
    print(exercicios_do_pdf())
    print()

    for nome, arquivo in (("Gene de exemplo", "gene_exemplo.txt"), ("Vírus", "virus.txt")):
        sequencia = ler_sequencia(DADOS / arquivo)
        print(formatar(analisar(nome, sequencia)))
        print()

    # Ciclo completo com arquivo: sequência -> .gbin -> sequência
    SAIDA.mkdir(exist_ok=True)
    virus = ler_sequencia(DADOS / "virus.txt")
    destino = SAIDA / "virus.gbin"
    GeneComprimido(virus).salvar(destino)
    recuperado = GeneComprimido.carregar(destino).descomprimir()
    print(f"Arquivo gerado: {destino.relative_to(RAIZ)} ({destino.stat().st_size} bytes)")
    print(f"Sequência lida de volta é idêntica à original: {'SIM' if recuperado == virus else 'NÃO'}")
    return 0 if recuperado == virus else 1

def cmd_comprimir(args) -> int:
    entrada = Path(args.entrada)
    saida = Path(args.saida) if args.saida else SAIDA / (entrada.stem + ".gbin")
    saida.parent.mkdir(parents=True, exist_ok=True)

    sequencia = ler_sequencia(entrada)
    GeneComprimido(sequencia).salvar(saida)
    print(f"{len(sequencia)} nucleotídeos -> {saida} ({saida.stat().st_size} bytes)")
    return 0


def cmd_descomprimir(args) -> int:
    entrada = Path(args.entrada)
    saida = Path(args.saida) if args.saida else SAIDA / (entrada.stem + "_descomprimido.txt")
    saida.parent.mkdir(parents=True, exist_ok=True)

    sequencia = GeneComprimido.carregar(entrada).descomprimir()
    saida.write_text(sequencia + "\n", encoding="utf-8")
    print(f"{len(sequencia)} nucleotídeos -> {saida}")
    return 0


def montar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compactação de sequências de DNA (2 bits por nucleotídeo).")
    sub = parser.add_subparsers(dest="comando")

    sub.add_parser("demo", help="Demonstração completa (padrão)").set_defaults(func=cmd_demo)
    sub.add_parser("exercicios", help="Contas de bits do PDF").set_defaults(func=cmd_exercicios)

    p = sub.add_parser("comprimir", help="Compacta um arquivo de sequência")
    p.add_argument("entrada", help="Arquivo .txt (puro ou FASTA)")
    p.add_argument("-o", "--saida", help="Arquivo .gbin de saída")
    p.set_defaults(func=cmd_comprimir)

    p = sub.add_parser("descomprimir", help="Descompacta um arquivo .gbin")
    p.add_argument("entrada", help="Arquivo .gbin")
    p.add_argument("-o", "--saida", help="Arquivo .txt de saída")
    p.set_defaults(func=cmd_descomprimir)
    return parser


def main() -> int:
    args = montar_parser().parse_args()
    func = getattr(args, "func", cmd_demo)
    try:
        return func(args)
    except (ValueError, OSError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
