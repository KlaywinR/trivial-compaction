# Compactação de Genes

Compacta sequências de DNA usando **2 bits por nucleotídeo** (A=00, C=01, G=10, T=11) em vez dos
8 bits de um caractere — economia de **75%**. Baseado em Kopec, *Problemas Clássicos de Ciência da
Computação com Python* (p. 36).

## Executar

```bash
python main.py                 # demonstração completa (exercícios do PDF, gene e vírus)
python main.py exercicios      # só as contas de bits do PDF
python -m unittest -v          # 22 testes

python main.py comprimir dados/virus.txt          # gera saida/virus.gbin
python main.py descomprimir saida/virus.gbin      # gera saida/virus_descomprimido.txt
```

Requisito: Python 3.10+ (sem bibliotecas externas).

## Estrutura

```
main.py          Ponto de entrada (linha de comando)
compactacao/     Lógica: codificacao, gene_comprimido, calculo_bits, sequencias, relatorio
dados/           gene_exemplo.txt e virus.txt (do PDF)
saida/           Arquivos gerados (.gbin, .txt)
testes/          Testes unittest
docs/            DOCUMENTACAO.md — explica o que cada arquivo e função faz
```

Veja **`docs/DOCUMENTACAO.md`** para a explicação detalhada de cada parte do código.
