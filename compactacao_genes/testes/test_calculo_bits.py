import unittest
from pathlib import Path

from compactacao import (
    bits_necessarios,
    contar_nucleotideos,
    economia_percentual,
    ler_sequencia,
    limpar_sequencia,
    tamanho_compactado_bits,
    tamanho_original_bits,
    validar_sequencia,
    valores_representaveis,
)

RAIZ = Path(__file__).resolve().parent.parent


class TestCalculoBits(unittest.TestCase):
    def test_valores_representaveis(self):
        self.assertEqual(valores_representaveis(2), 4)
        self.assertEqual(valores_representaveis(3), 8)

    def test_bits_necessarios(self):
        self.assertEqual(bits_necessarios(1), 0)
        self.assertEqual(bits_necessarios(2), 1)
        self.assertEqual(bits_necessarios(4), 2)
        self.assertEqual(bits_necessarios(5), 3)
        self.assertEqual(bits_necessarios(8), 3)

    def test_bits_necessarios_invalido(self):
        with self.assertRaises(ValueError):
            bits_necessarios(0)

    def test_exercicio_acgt(self):
        self.assertEqual(tamanho_original_bits(4), 32)
        self.assertEqual(tamanho_compactado_bits(4, 4), 8)

    def test_exercicio_abcdefgh(self):
        self.assertEqual(tamanho_original_bits(8), 64)
        self.assertEqual(tamanho_compactado_bits(8, 8), 24)

    def test_economia_percentual(self):
        self.assertEqual(economia_percentual(32, 8), 75.0)
        with self.assertRaises(ValueError):
            economia_percentual(0, 0)


class TestSequencias(unittest.TestCase):
    def test_limpar_remove_cabecalho_e_espacos(self):
        texto = ">seq1 exemplo\nacg t\nTTA\n"
        self.assertEqual(limpar_sequencia(texto), "ACGTTTA")

    def test_validar(self):
        validar_sequencia("ACGT")
        with self.assertRaises(ValueError):
            validar_sequencia("ACGN")

    def test_contagem(self):
        self.assertEqual(contar_nucleotideos("AACGT"), {"A": 2, "C": 1, "G": 1, "T": 1})

    def test_arquivo_do_virus_so_tem_acgt(self):
        virus = ler_sequencia(RAIZ / "dados" / "virus.txt")
        self.assertGreater(len(virus), 2000)
        self.assertEqual(set(virus), {"A", "C", "G", "T"})


if __name__ == "__main__":
    unittest.main()
