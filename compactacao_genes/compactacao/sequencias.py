from collections import Counter
from pathlib import Path

from .codificacao import NUCLEOTIDEO_PARA_BITS


def limpar_sequencia(texto: str) -> str:
    linhas = [linha for linha in texto.splitlines() if not linha.lstrip().startswith(">")]
    return "".join("".join(linhas).split()).upper()

def validar_sequencia(sequencia: str) -> None:
    invalidos = sorted(set(sequencia) - set(NUCLEOTIDEO_PARA_BITS))
    if invalidos:
        raise ValueError(f"Caracteres inválidos na sequência: {invalidos}")

def ler_sequencia(caminho: str | Path) -> str:
    texto = Path(caminho).read_text(encoding="utf-8")
    sequencia = limpar_sequencia(texto)
    validar_sequencia(sequencia)
    return sequencia

def contar_nucleotideos(sequencia: str) -> dict[str, int]:
    contagem = Counter(sequencia)
    return {nuc: contagem.get(nuc, 0) for nuc in NUCLEOTIDEO_PARA_BITS}
