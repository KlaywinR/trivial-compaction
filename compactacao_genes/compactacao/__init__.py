"""Pacote de compactação de sequências de DNA."""

from .calculo_bits import (
    bits_necessarios,
    economia_percentual,
    tamanho_compactado_bits,
    tamanho_original_bits,
    valores_representaveis,
)
from .gene_comprimido import GeneComprimido
from .sequencias import (
    contar_nucleotideos,
    ler_sequencia,
    limpar_sequencia,
    validar_sequencia,
)

__all__ = [
    "GeneComprimido",
    "bits_necessarios",
    "contar_nucleotideos",
    "economia_percentual",
    "ler_sequencia",
    "limpar_sequencia",
    "tamanho_compactado_bits",
    "tamanho_original_bits",
    "validar_sequencia",
    "valores_representaveis",
]
