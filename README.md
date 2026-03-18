# Relatório da Atividade 2 — Soma de Valores em Paralelo

**Disciplina:** Computação Paralela e Distribuída
**Aluno(s):** Matheus Nery Walkowicz
**Turma:** Noturno
**Professor:** Rafael Marconi Ramos
**Data:** 2026

---

# 1. Descrição do Problema

O problema consiste em **somar um grande conjunto de valores inteiros** armazenados em arquivos de texto, onde cada linha contém um número. A tarefa foi implementada de duas formas: serial e paralela, com o objetivo de comparar o desempenho entre as abordagens.

**Qual problema foi implementado:**
Soma de 1.000.000 (numero1.txt) e 10.000.000 (numero2.txt) de números inteiros lidos de arquivo, além do desafio final com 1.000.000.000 de números (numerogigante.txt).

**Qual algoritmo foi utilizado:**
Soma acumulativa com divisão do arquivo em fatias por offset de bytes. Cada processo recebe o offset de início e fim no arquivo, abre o arquivo independentemente e realiza a soma de sua fatia. Ao final, o processo principal agrega os resultados parciais.

**Tamanhos de entrada:**
- numero1.txt: 1.000.000 de números — Soma: -88
- numero2.txt: 10.000.000 de números — Soma: -2.120.566
- numerogigante.txt: 1.000.000.000 de números — Soma: 17.178

**Complexidade aproximada:** O(n) — linear no número de elementos.

---

# 2. Ambiente Experimental

| Item                        | Descrição                                   |
| --------------------------- | ------------------------------------------- |
| Processador                 | Intel Core i7-12700 12ª Geração — 2,10 GHz                                           |
| Número de núcleos           | 12 núcleos físicos (8P + 4E) / 20 threads                                           |
| Memória RAM                 | 16,0 GB                                           |
| Sistema Operacional         | Windows                                     |
| Linguagem utilizada         | Python 3                                    |
| Biblioteca de paralelização | multiprocessing (módulo nativo do Python)   |
| Compilador / Versão         | Python 3.x                                  |

---

# 3. Metodologia de Testes

O tempo foi medido com `time.perf_counter()`. A divisão paralela é feita por offset de bytes no arquivo — cada processo avança até o próximo `\n` para não cortar um número, e lê em blocos de 8 MB.

### Configurações testadas

- 1 processo (serial)
- 2 processos
- 4 processos
- 8 processos
- 12 processos

---

# 4. Resultados Experimentais

## numero1.txt — 1.000.000 de números

| Nº Processos | Tempo (s) |
| ------------ | --------- |
| 1 (serial)   | 0,1024    |
| 2            | 0,2959    |
| 4            | 0,3631    |
| 8            | 0,4644    |
| 12           | 0,1611    |

## numero2.txt — 10.000.000 de números

| Nº Processos | Tempo (s) |
| ------------ | --------- |
| 1 (serial)   | 1,9712    |
| 2            | 2,3582    |
| 4            | 2,5841    |
| 8            | 2,8142    |
| 12           | 3,0359    |

---

# 5. Cálculo de Speedup e Eficiência

### Speedup

```
Speedup(p) = T(1) / T(p)
```

### Eficiência

```
Eficiência(p) = Speedup(p) / p
```

---

# 6. Tabela de Resultados

## numero1.txt | T(1) = 0,1024s

| Processos  | Tempo (s) | Speedup | Eficiência |
| ---------- | --------- | ------- | ---------- |
| 1 (serial) | 0,1024    | 1,00    | 1,0000     |
| 2          | 0,2959    | 0,35    | 0,1732     |
| 4          | 0,3631    | 0,28    | 0,0705     |
| 8          | 0,4644    | 0,22    | 0,0275     |
| 12         | 0,1611    | 0,64    | 0,0531     |

## numero2.txt | T(1) = 1,9712s

| Processos  | Tempo (s) | Speedup | Eficiência |
| ---------- | --------- | ------- | ---------- |
| 1 (serial) | 1,9712    | 1,00    | 1,0000     |
| 2          | 2,3582    | 0,84    | 0,4177     |
| 4          | 2,5841    | 0,76    | 0,1905     |
| 8          | 2,8142    | 0,70    | 0,0875     |
| 12         | 3,0359    | 0,65    | 0,0541     |

---

# 7. Gráfico de Tempo de Execução

> Disponível na planilha resultados_soma_paralela.xlsx, aba Gráfico Tempo.

- Eixo X: número de processos
- Eixo Y: tempo de execução (segundos)

---

# 8. Gráfico de Speedup

> Disponível na planilha resultados_soma_paralela.xlsx, aba Speedup e Eficiência.

- Eixo X: número de processos
- Eixo Y: speedup obtido vs speedup ideal

---

# 9. Gráfico de Eficiência

> Disponível na planilha resultados_soma_paralela.xlsx, aba Speedup e Eficiência.

- Eixo X: número de processos
- Eixo Y: eficiência (0 a 1)

---

# 10. Análise dos Resultados

**O speedup foi próximo do ideal?**
Não. O speedup ideal com 2 processos seria 2,0x. Os valores obtidos ficaram abaixo de 1,0 na maioria dos casos, indicando que a versão paralela foi mais lenta que a serial.

**A aplicação apresentou escalabilidade?**
Não. O tempo aumentou progressivamente com mais processos (1,97s → 3,03s para numero2.txt), demonstrando que o overhead superou qualquer ganho paralelo.

**Em qual ponto a eficiência começou a cair?**
Já com 2 processos a eficiência é baixa (42% para numero2.txt, 17% para numero1.txt), caindo para menos de 6% com 12 processos.

**Houve overhead de paralelização?**
Sim, significativo. O Python `multiprocessing` cria processos separados (não threads), com custo de criação e comunicação via Queue maior que threads nativas. Cada processo abre o arquivo independentemente, gerando contenção no disco.

**Causas para perda de desempenho:**
- Gargalo de I/O: leitura do arquivo domina ~95% do tempo total.
- Overhead de processos: criação e comunicação entre processos tem custo fixo alto no Python.
- Lei de Amdahl: a fração serial (abertura e leitura do arquivo) limita o ganho máximo independente do número de processos.
- Contenção de disco: múltiplos processos lendo o mesmo arquivo simultaneamente competem pelo mesmo recurso.

---

# 11. Conclusão

Os experimentos demonstraram que, para soma de valores em arquivo com Python `multiprocessing`, o paralelismo não trouxe ganho de desempenho nas configurações testadas. A versão serial foi mais rápida em quase todos os cenários.

O gargalo principal é o I/O de leitura do arquivo, operação sequencial que domina o tempo total. Adicionalmente, o modelo de processos do Python tem overhead maior que threads nativas, o que agrava ainda mais a situação para arquivos de tamanho médio.

**Melhor configuração:** Serial (0,1024s para 1M e 1,9712s para 10M).

**Desafio Final — numerogigante.txt (1 bilhão de números):**

| Implementação  | Soma   | Tempo  |
|----------------|--------|--------|
| Python (12p.)  | 17.178 | 46,38s |
| Enunciado ref. | ***    | 78,00s |

A implementação Python processou 1 bilhão de números em 46 segundos, sendo ~1,68x mais rápida que a referência do enunciado (78s), graças à leitura paralela por blocos de 8 MB sem carregar o arquivo inteiro na memória.

**Melhorias possíveis:**
- Usar `numpy` para leitura e soma vetorizada.
- Explorar `mmap` (memory-mapped files) para leitura mais eficiente.
- Usar `concurrent.futures.ProcessPoolExecutor` para gerenciamento otimizado de processos.
- Para arquivos muito grandes, avaliar bibliotecas como `pandas` ou `polars` com suporte nativo a leitura paralela.
