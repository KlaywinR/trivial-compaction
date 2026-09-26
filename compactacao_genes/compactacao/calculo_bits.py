"""
Regra geral: com N bits é possível representar 2^N valores diferentes.
Logo, para representar `n` valores distintos, precisamos do menor N tal que
2^N >= n.
"""

from .codificacao import BITS_POR_CARACTERE

def valores_representaveis(bits: int) -> int:
    """Quantos valores diferentes cabem em `bits` bits (2^bits)."""
    if bits < 0:
        raise ValueError("A quantidade de bits não pode ser negativa.")
    return 2 ** bits

def bits_necessarios(qtd_valores: int) -> int:
    """Menor quantidade de bits capaz de representar `qtd_valores` valores.
    Exemplos: 4 -> 2 bits, e assim por diante.
    """
    if qtd_valores < 1:
        raise ValueError("É preciso ao menos 1 valor.")
    return (qtd_valores - 1).bit_length()

def tamanho_original_bits(qtd_simbolos: int, bits_por_caractere: int = BITS_POR_CARACTERE) -> int:
    """String possuindo um  tamanho de 8 caracteres de forma padronizada."""
    return qtd_simbolos * bits_por_caractere

def tamanho_compactado_bits(qtd_simbolos: int, tamanho_alfabeto: int) -> int:
    """Tamanho após compactar; usando o mínimo de bits por símbolo do alfabeto."""
    return qtd_simbolos * bits_necessarios(tamanho_alfabeto)

def economia_percentual(original: int, compactado: int) -> float:
    """Percentual de espaço economizado."""
    if original <= 0:
        raise ValueError("O tamanho original deve ser positivo.")
    return (1 - compactado / original) * 100
