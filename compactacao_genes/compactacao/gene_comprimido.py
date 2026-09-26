"""Classe GeneComprimido: guarda um gene usando apenas 2 bits por nucleotídeo.

Ideia central (Kopec, cap. 1): a sequência inteira é armazenada em UM único
número inteiro. Python permite inteiros de tamanho arbitrário, então o número
cresce conforme o gene cresce.

Um bit "sentinela" (o número 1) é colocado na frente de tudo. Ele é
necessário porque inteiros não guardam zeros à esquerda: sem o sentinela, o
gene "A" (00) e o gene "AA" (0000) seriam ambos o número 0 e não seria
possível saber o tamanho original.
"""

from pathlib import Path

from .codificacao import (
    BITS_PARA_NUCLEOTIDEO,
    BITS_POR_NUCLEOTIDEO,
    NUCLEOTIDEO_PARA_BITS,
)

_MASCARA = (1 << BITS_POR_NUCLEOTIDEO) - 1  # 0b11: isola os 2 bits do "topo"


class GeneComprimido:

    def __init__(self, gene: str = "") -> None:
        """Compacta a string `gene`."""
        self._bits = self._comprimir(gene)


    @staticmethod
    def _comprimir(gene: str) -> int:
        bits = 1  # bit sentinela
        for posicao, nucleotideo in enumerate(gene.upper()):
            codigo = NUCLEOTIDEO_PARA_BITS.get(nucleotideo)
            if codigo is None:
                raise ValueError(
                    f"Nucleotídeo inválido {nucleotideo!r} na posição {posicao}. "
                    "Use apenas A, C, G ou T."
                )
            bits = (bits << BITS_POR_NUCLEOTIDEO) | codigo  # abre 2 bits e encaixa o código
        return bits

    def descomprimir(self) -> str:
        """Reconstrói a string original a partir dos bits."""
        total = len(self)
        letras = []
        for i in range(total):
            # O primeiro nucleotídeo está nos bits mais altos (logo abaixo do sentinela)
            deslocamento = (total - 1 - i) * BITS_POR_NUCLEOTIDEO
            codigo = (self._bits >> deslocamento) & _MASCARA
            letras.append(BITS_PARA_NUCLEOTIDEO[codigo])
        return "".join(letras)

    def __len__(self) -> int:
        """Quantidade de nucleotídeos."""
        return (self._bits.bit_length() - 1) // BITS_POR_NUCLEOTIDEO

    @property
    def tamanho_em_bits(self) -> int:
        """Bits usados só pelos dados, sem bit de sentinela."""
        return self._bits.bit_length() - 1

    @property
    def inteiro(self) -> int:
        """O número inteiro que guarda tudo - inclui o bit sentinela."""
        return self._bits

    def como_bits(self) -> str:
        """Devolve os bits como texto, ex.: 'ATG' -> '001110'."""
        return format(self._bits, "b")[1:]

    def __str__(self) -> str:
        return self.descomprimir()

    def __repr__(self) -> str:
        return f"GeneComprimido(nucleotideos={len(self)}, bits={self.tamanho_em_bits})"

    def __eq__(self, outro: object) -> bool:
        return isinstance(outro, GeneComprimido) and self._bits == outro._bits

    def __hash__(self) -> int:
        return hash(self._bits)
    
    def para_bytes(self) -> bytes:
        """Serializa o inteiro em bytes. O sentinela preserva o tamanho."""
        quantidade = (self._bits.bit_length() + 7) // 8
        return self._bits.to_bytes(quantidade, "big")

    @classmethod
    def de_bytes(cls, dados: bytes) -> "GeneComprimido":
        """Reconstrói um GeneComprimido a partir de bytes gerados por `para_bytes`."""
        if not dados:
            raise ValueError("Dados vazios: não é um gene compactado válido.")
        bits = int.from_bytes(dados, "big")
        if bits == 0 or (bits.bit_length() - 1) % BITS_POR_NUCLEOTIDEO != 0:
            raise ValueError("Dados corrompidos: não é um gene compactado válido.")
        gene = cls()
        gene._bits = bits
        return gene

    def salvar(self, caminho: str | Path) -> None:
        """Grava o gene compactado em um arquivo binário."""
        Path(caminho).write_bytes(self.para_bytes())

    @classmethod
    def carregar(cls, caminho: str | Path) -> "GeneComprimido":
        """Lê um arquivo .gbin e devolve o GeneComprimido."""
        return cls.de_bytes(Path(caminho).read_bytes())
