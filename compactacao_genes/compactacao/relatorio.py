from dataclasses import dataclass

from .calculo_bits import (
    bits_necessarios,
    economia_percentual,
    tamanho_compactado_bits,
    tamanho_original_bits,
    valores_representaveis,
)
from .codificacao import BITS_POR_CARACTERE
from .gene_comprimido import GeneComprimido
from .sequencias import contar_nucleotideos


@dataclass(frozen=True)
class ResultadoCompactacao:
    nome: str
    qtd_nucleotideos: int
    bits_original: int
    bits_compactado: int
    economia_percentual: float
    bytes_original: int
    bytes_arquivo: int
    contagem: dict
    integridade_ok: bool

def analisar(nome: str, sequencia: str) -> ResultadoCompactacao:
    sequencia = sequencia.upper()
    gene = GeneComprimido(sequencia)
    return ResultadoCompactacao(
        nome=nome,
        qtd_nucleotideos=len(gene),
        bits_original=tamanho_original_bits(len(sequencia)),
        bits_compactado=gene.tamanho_em_bits,
        economia_percentual=economia_percentual(
            tamanho_original_bits(len(sequencia)), gene.tamanho_em_bits
        ) if sequencia else 0.0,
        bytes_original=len(sequencia), 
        bytes_arquivo=len(gene.para_bytes()),
        contagem=contar_nucleotideos(sequencia),
        integridade_ok=gene.descomprimir() == sequencia,
    )

def formatar(r: ResultadoCompactacao) -> str:
    contagem = "  ".join(f"{nuc}={qtd}" for nuc, qtd in r.contagem.items())
    return "\n".join([
        f"=== {r.nome} ===",
        f"Nucleotídeos ............ {r.qtd_nucleotideos}",
        f"Composição .............. {contagem}",
        f"Como string (8 bits/nuc). {r.bits_original} bits ({r.bytes_original} bytes)",
        f"Compactado (2 bits/nuc).. {r.bits_compactado} bits",
        f"Em arquivo binário ...... {r.bytes_arquivo} bytes",
        f"Economia ................ {r.economia_percentual:.2f}%",
        f"Descompactação idêntica . {'SIM' if r.integridade_ok else 'NÃO'}",
    ])


def _linha_exercicio(texto: str) -> str:
    alfabeto = len(set(texto))
    bits_simbolo = bits_necessarios(alfabeto)
    original = tamanho_original_bits(len(texto))
    compactado = tamanho_compactado_bits(len(texto), alfabeto)
    return (
        f"{texto} -> {original} bits como string ({len(texto)} x {BITS_POR_CARACTERE}); "
        f"{compactado} bits compactado ({len(texto)} x {bits_simbolo})"
    )


def exercicios_do_pdf() -> str:
    atg = GeneComprimido("ATG")
    return "\n".join([
        "--- Exercícios Testes  ---",
        _linha_exercicio("ACGT"),
        f"2 bits: 00, 01, 10, 11 -> 2^2 -> {valores_representaveis(2)}",
        _linha_exercicio("ABCDEFGH"),
        f"3 bits: 000..111 -> 2^3 -> {valores_representaveis(3)}",
        "",
        "Figura do livro (Kopec, p. 36):",
        f"'ATG' em formato de string: {tamanho_original_bits(3)} bits",
        f"'ATG' em arquivo compactado : {atg.como_bits()} ({atg.tamanho_em_bits} bits",
        f"Descompactado    : {atg.descomprimir()}",
    ])
