"""Tabela de codificação usada na compactação de DNA.

Cada nucleotídeo só assume 4 valores diferentes.
Como 2 bits representam exatamente 4 valores (2^2 = 4), basta 2 bits por
nucleotídeo, em vez dos 8 bits que um caractere de texto costuma ocupar.
"""

# O nucleotídeo é composto por 2 bits.
NUCLEOTIDEO_PARA_BITS = {
    "A": 0b00,
    "C": 0b01,
    "G": 0b10,
    "T": 0b11,
}

# Nucleotídeo que é uma tabela inversa, sendo usada na descompactação
BITS_PARA_NUCLEOTIDEO = {bits: nuc for nuc, bits in NUCLEOTIDEO_PARA_BITS.items()}

BITS_POR_NUCLEOTIDEO = 2  
BITS_POR_CARACTERE = 8   
