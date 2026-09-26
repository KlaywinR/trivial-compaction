# Documentação — Compactação de Genes (2 bits por nucleotídeo)

Implementação em Python do projeto "Compactação Trivial / Economizar espaço", baseada em
Kopec, *Problemas Clássicos de Ciência da Computação com Python* (p. 36).

---

## 1. A ideia em poucas linhas

- Um caractere de texto (string) costuma ocupar **8 bits**.
- Um nucleotídeo só pode ser **A, C, G ou T** → apenas **4 valores possíveis**.
- Com **2 bits** cabem exatamente 4 valores (2² = 4): `00`, `01`, `10`, `11`.
- Logo, cada nucleotídeo pode ser guardado em 2 bits em vez de 8: **economia de 75%**.

| Nucleotídeo | Código |
|:-----------:|:------:|
| A | `00` |
| C | `01` |
| G | `10` |
| T | `11` |

### As contas do PDF

| Texto | Como string | Compactado | Motivo |
|-------|------------:|-----------:|--------|
| `ACGT` | 4 × 8 = **32 bits** | 4 × 2 = **8 bits** | 4 símbolos → 2 bits (2² = 4) |
| `ABCDEFGH` | 8 × 8 = **64 bits** | 8 × 3 = **24 bits** | 8 símbolos → 3 bits (2³ = 8) |

Regra geral: para `n` símbolos diferentes, usa-se o menor `N` tal que `2^N >= n`.

---

## 2. Estrutura de diretórios

```
compactacao_genes/
├── main.py                       # Ponto de entrada (linha de comando)
├── README.md                     # Resumo e como executar
├── compactacao/                  # Pacote com a lógica do projeto
│   ├── __init__.py               # Exporta a API pública do pacote
│   ├── codificacao.py            # Tabela A/C/G/T <-> 2 bits
│   ├── gene_comprimido.py        # Classe GeneComprimido (o coração do projeto)
│   ├── calculo_bits.py           # Contas de quantos bits cada alfabeto precisa
│   ├── sequencias.py             # Ler/limpar/validar arquivos de sequência
│   └── relatorio.py              # Relatórios comparativos e exercícios do PDF
├── dados/
│   ├── gene_exemplo.txt          # Gene de exemplo do PDF (86 nucleotídeos)
│   └── virus.txt                 # Sequência do vírus do PDF (2689 nucleotídeos)
├── saida/                        # Onde ficam os arquivos gerados (.gbin, .txt)
├── testes/
│   ├── test_gene_comprimido.py   # Testes da compactação/descompactação
│   └── test_calculo_bits.py      # Testes das contas de bits e da leitura de arquivos
└── docs/
    └── DOCUMENTACAO.md           # Este documento
```

---

## 3. O que cada arquivo faz

### 3.1 `compactacao/codificacao.py`

Define as constantes usadas por todo o projeto:

| Nome | O que é |
|------|---------|
| `NUCLEOTIDEO_PARA_BITS` | Dicionário `{"A": 0b00, "C": 0b01, "G": 0b10, "T": 0b11}`. Usado ao **compactar**. |
| `BITS_PARA_NUCLEOTIDEO` | Dicionário inverso (`0b00 → "A"` ...), gerado automaticamente a partir do primeiro. Usado ao **descompactar**. |
| `BITS_POR_NUCLEOTIDEO` | `2` — tamanho do código de cada nucleotídeo. |
| `BITS_POR_CARACTERE` | `8` — custo de um caractere numa string (base de comparação). |

Se quiser mudar a codificação (por exemplo, trocar a ordem dos códigos), este é o único lugar a editar.

### 3.2 `compactacao/gene_comprimido.py`

Contém a classe **`GeneComprimido`**, que guarda o gene inteiro **em um único número inteiro**
(Python aceita inteiros de tamanho ilimitado).

**O bit sentinela.** O número começa em `1` antes de qualquer nucleotídeo. Inteiros não guardam zeros à
esquerda, então sem esse `1` os genes `"A"` (`00`) e `"AA"` (`0000`) virariam ambos o número 0 e o tamanho
original se perderia. O sentinela marca onde os dados começam.

| Membro | O que faz |
|--------|-----------|
| `__init__(gene="")` | Recebe a string e chama `_comprimir`. Aceita maiúsculas e minúsculas. |
| `_comprimir(gene)` | Começa com `bits = 1` e, para cada nucleotídeo, **abre 2 bits** (`bits << 2`) e **encaixa o código** (`| codigo`). Levanta `ValueError` (com a posição) se aparecer algo além de A, C, G, T. |
| `descomprimir()` | Faz o caminho inverso: para cada posição, desloca os bits (`>>`) e aplica a máscara `0b11` para isolar 2 bits; traduz cada código de volta para a letra. Devolve a string original. |
| `__len__()` | Número de nucleotídeos = `(bit_length - 1) // 2` (o `- 1` desconta o sentinela). |
| `tamanho_em_bits` | Bits usados só pelos dados (2 × nº de nucleotídeos), sem o sentinela. |
| `inteiro` | O número inteiro que guarda tudo (com o sentinela). |
| `como_bits()` | Os bits em texto, sem o sentinela. Ex.: `"ATG"` → `"001110"`. |
| `__str__()` | Devolve o gene descompactado. |
| `__repr__()` | Resumo, ex.: `GeneComprimido(nucleotideos=86, bits=172)`. |
| `__eq__()` / `__hash__()` | Dois `GeneComprimido` são iguais se guardam o mesmo inteiro. |
| `para_bytes()` | Converte o inteiro em bytes (big-endian) para gravar em disco. |
| `de_bytes(dados)` | Reconstrói o objeto a partir de bytes. Levanta `ValueError` se os dados forem vazios ou estiverem corrompidos. |
| `salvar(caminho)` | Grava `para_bytes()` em um arquivo `.gbin`. |
| `carregar(caminho)` | Lê um `.gbin` e devolve o `GeneComprimido`. |

#### Exemplo passo a passo: `"ATG"`

Compactando (A=`00`, T=`11`, G=`10`):

```
início:            1                 (sentinela)
lê 'A': (1 << 2) | 00   →  100
lê 'T': (100 << 2) | 11 →  10011
lê 'G': (10011 << 2) | 10 → 1001110
```

Resultado: `1001110` (7 bits). Sem o sentinela restam **`001110`** — exatamente a figura do livro
(2 + 2 + 2 = 6 bits, contra 8 + 8 + 8 = 24 bits da string).

Descompactando (`total = (7 - 1) // 2 = 3` nucleotídeos):

```
i=0: 1001110 >> 4 = 100 → & 11 = 00 → A
i=1: 1001110 >> 2 = 10011 → & 11 = 11 → T
i=2: 1001110 >> 0 → & 11 = 10 → G
```

Resultado: `ATG`.

### 3.3 `compactacao/calculo_bits.py`

Funções de "matemática dos bits" (as contas do PDF):

| Função | O que faz | Exemplo |
|--------|-----------|---------|
| `valores_representaveis(bits)` | Quantos valores cabem em `bits` bits (2^bits). | `valores_representaveis(3)` → `8` |
| `bits_necessarios(qtd_valores)` | Menor nº de bits para `qtd_valores` valores. Usa `(n - 1).bit_length()`, que equivale a ⌈log₂ n⌉ sem erros de ponto flutuante. | `bits_necessarios(4)` → `2`; `bits_necessarios(5)` → `3` |
| `tamanho_original_bits(qtd, bits_por_caractere=8)` | Tamanho como string. | `tamanho_original_bits(4)` → `32` |
| `tamanho_compactado_bits(qtd, tamanho_alfabeto)` | Tamanho compactado usando o mínimo de bits por símbolo. | `tamanho_compactado_bits(8, 8)` → `24` |
| `economia_percentual(original, compactado)` | Percentual economizado. | `economia_percentual(32, 8)` → `75.0` |

### 3.4 `compactacao/sequencias.py`

Cuida dos arquivos de texto com sequências:

| Função | O que faz |
|--------|-----------|
| `limpar_sequencia(texto)` | Remove linhas de cabeçalho FASTA (que começam com `>`), espaços e quebras de linha; converte para maiúsculas. É por isso que o `virus.txt`, dividido em várias linhas, vira uma sequência contínua. |
| `validar_sequencia(seq)` | Levanta `ValueError` se houver caractere diferente de A, C, G, T. |
| `ler_sequencia(caminho)` | Lê o arquivo, limpa e valida. É a função usada pelo `main.py`. |
| `contar_nucleotideos(seq)` | Conta quantos A, C, G e T existem (usado no relatório). |

### 3.5 `compactacao/relatorio.py`

Gera as saídas mostradas no terminal:

| Item | O que faz |
|------|-----------|
| `ResultadoCompactacao` | Dataclass que guarda os números de uma compactação (tamanhos, economia, composição, integridade). |
| `analisar(nome, sequencia)` | Compacta, descompacta e **confere** se o resultado é idêntico ao original. Devolve um `ResultadoCompactacao`. |
| `formatar(resultado)` | Transforma o resultado em texto legível. |
| `exercicios_do_pdf()` | Reproduz as contas do PDF (`ACGT`, `ABCDEFGH`, 2 bits → 4 valores, 3 bits → 8 valores e a figura `ATG` → `001110`). |

### 3.6 `compactacao/__init__.py`

Transforma a pasta em pacote Python e exporta os nomes principais (`GeneComprimido`, `ler_sequencia`,
`bits_necessarios` etc.), permitindo escrever `from compactacao import GeneComprimido`.

### 3.7 `main.py`

Interface de linha de comando (usa `argparse`):

| Comando | O que faz |
|---------|-----------|
| `python main.py` ou `python main.py demo` | Roda tudo: exercícios do PDF, relatório do gene de exemplo e do vírus, e grava/lê `saida/virus.gbin` para provar que o ciclo completo funciona. |
| `python main.py exercicios` | Só as contas de bits do PDF. |
| `python main.py comprimir ARQ [-o SAIDA.gbin]` | Compacta um arquivo de sequência (padrão de saída: `saida/<nome>.gbin`). |
| `python main.py descomprimir ARQ.gbin [-o SAIDA.txt]` | Reconstrói o texto da sequência. |

Erros de arquivo/sequência inválida são mostrados como `Erro: ...` e o programa termina com código 1.

### 3.8 `dados/`

- `gene_exemplo.txt` — o gene do PDF (`TAGGGATTAACC...GATTATA`), 86 nucleotídeos.
- `virus.txt` — a sequência do vírus do PDF, 2689 nucleotídeos (mantida com as quebras de linha do PDF;
  `limpar_sequencia` junta tudo).

### 3.9 `testes/`

Usam apenas a biblioteca padrão (`unittest`). Rodam com `python -m unittest -v` na raiz do projeto.

| Arquivo | O que verifica |
|---------|----------------|
| `test_gene_comprimido.py` | Ida e volta do gene e do vírus; a figura `ATG` → `001110`; minúsculas; gene vazio; `"A"` ≠ `"AA"` (sentinela); erro em letra inválida; bytes/arquivo ida e volta; dados corrompidos; arquivo menor que o texto. |
| `test_calculo_bits.py` | Contas de bits (`ACGT`, `ABCDEFGH`, 2²=4, 2³=8); economia de 75%; limpeza/validação/contagem de sequências; `virus.txt` só com A, C, G, T. |

---

## 4. Resultados obtidos

| Sequência | Nucleotídeos | Como string | Compactado (dados) | Arquivo `.gbin` | Economia |
|-----------|-------------:|------------:|-------------------:|----------------:|---------:|
| Gene de exemplo | 86 | 688 bits (86 bytes) | 172 bits | 22 bytes | 75% |
| Vírus | 2689 | 21512 bits (2689 bytes) | 5378 bits | 673 bytes | 75% |

O arquivo `.gbin` é um pouco maior que `bits / 8` porque inclui o **bit sentinela** e é **arredondado
para um número inteiro de bytes** (5378 bits + 1 = 5379 bits → 673 bytes).

---

## 5. Como executar

```bash
cd compactacao_genes
python main.py                 
python main.py exercicios     
python -m unittest -v        
python main.py comprimir dados/virus.txt
python main.py descomprimir saida/virus.gbin
```
---

## 6. Limitações e possíveis extensões

- Só aceita **A, C, G, T**. Bases ambíguas de arquivos reais (como `N`) geram `ValueError`; para
  suportá-las seria preciso um alfabeto maior (3 bits) ou uma lista de exceções.
- A compactação por deslocamento de bits em um inteiro gigante é didática, mas tem custo
  quadrático para genomas muito grandes; para milhões de bases, o ideal seria processar em blocos
  (por exemplo, 4 nucleotídeos por byte).
- Esta é uma compactação **trivial** (tamanho fixo por símbolo). Métodos como Huffman ou
  LZ77 aproveitam repetições e frequências para comprimir ainda mais.
