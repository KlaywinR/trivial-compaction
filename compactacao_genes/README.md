# Compactação de Genes

Compacta sequências de DNA usando 2 bits por nucleotídeo (A=00, C=01, G=10, T=11) em vez dos
8 bits de um caractere — economia de 75%. Baseado em Kopec, *Problemas Clássicos de Ciência da
Computação com Python* (p. 36).

## Executar

```bash
python main.py                
python main.py exercicios      
python -m unittest -v          

python main.py comprimir dados/virus.txt          
python main.py descomprimir saida/virus.gbin     
```

## Estrutura

```
main.py          Ponto de entrada (linha de comando)
compactacao/     Lógica: codificacao, gene_comprimido, calculo_bits, sequencias, relatorio
dados/           gene_exemplo.txt e virus.txt (do PDF)
saida/           Arquivos gerados (.gbin, .txt)
testes/          Testes unittest
docs/            DOCUMENTACAO.md — explica o que cada arquivo e função faz
```

Veja docs/DOCUMENTACAO.md para a explicação detalhada de cada parte do código.
