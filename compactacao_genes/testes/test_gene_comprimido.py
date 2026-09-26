import tempfile
import unittest
from pathlib import Path

from compactacao import GeneComprimido, ler_sequencia

RAIZ = Path(__file__).resolve().parent.parent

GENE_PDF = (
    "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAG"
    "CCATGGATCGATTATA"
)


class TestGeneComprimido(unittest.TestCase):
    def test_ida_e_volta_gene_do_pdf(self):
        self.assertEqual(GeneComprimido(GENE_PDF).descomprimir(), GENE_PDF)

    def test_ida_e_volta_virus(self):
        virus = ler_sequencia(RAIZ / "dados" / "virus.txt")
        self.assertEqual(GeneComprimido(virus).descomprimir(), virus)

    def test_figura_do_livro_atg(self):
        # A=00, T=11, G=10 -> 001110 (6 bits)
        gene = GeneComprimido("ATG")
        self.assertEqual(gene.como_bits(), "001110")
        self.assertEqual(gene.tamanho_em_bits, 6)

    def test_minusculas_sao_aceitas(self):
        self.assertEqual(str(GeneComprimido("acgt")), "ACGT")

    def test_gene_vazio(self):
        gene = GeneComprimido("")
        self.assertEqual(len(gene), 0)
        self.assertEqual(gene.descomprimir(), "")

    def test_a_e_aa_sao_diferentes(self):
        # Garante que o bit sentinela preserva o tamanho (zeros à esquerda)
        self.assertNotEqual(GeneComprimido("A"), GeneComprimido("AA"))
        self.assertEqual(len(GeneComprimido("AAAA")), 4)

    def test_tamanho_em_bits_e_duas_vezes_o_tamanho(self):
        gene = GeneComprimido(GENE_PDF)
        self.assertEqual(len(gene), len(GENE_PDF))
        self.assertEqual(gene.tamanho_em_bits, 2 * len(GENE_PDF))

    def test_nucleotideo_invalido(self):
        with self.assertRaises(ValueError):
            GeneComprimido("ACGX")

    def test_bytes_ida_e_volta_varios_tamanhos(self):
        base = "ACGT" * 10
        for tamanho in range(0, 30):
            gene = base[:tamanho]
            with self.subTest(tamanho=tamanho):
                recuperado = GeneComprimido.de_bytes(GeneComprimido(gene).para_bytes())
                self.assertEqual(recuperado.descomprimir(), gene)

    def test_de_bytes_invalido(self):
        with self.assertRaises(ValueError):
            GeneComprimido.de_bytes(b"")
        with self.assertRaises(ValueError):
            GeneComprimido.de_bytes(b"\x00")
        with self.assertRaises(ValueError):
            GeneComprimido.de_bytes(b"\x02")  # 10 -> 1 bit de dados (ímpar)

    def test_salvar_e_carregar_arquivo(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "gene.gbin"
            GeneComprimido(GENE_PDF).salvar(caminho)
            self.assertEqual(GeneComprimido.carregar(caminho).descomprimir(), GENE_PDF)

    def test_arquivo_e_menor_que_o_texto(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "gene.gbin"
            GeneComprimido(GENE_PDF).salvar(caminho)
            self.assertLess(caminho.stat().st_size, len(GENE_PDF))


if __name__ == "__main__":
    unittest.main()
