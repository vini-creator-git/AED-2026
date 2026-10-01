# Explicacao do programa de DNA e RNA

Este documento reúne as explicacoes do programa que sorteia uma fita de DNA e, se o usuario quiser, cria a fita correspondente de RNA.

## 1. Importando o sorteio

```python
from random import *
```

Importa as funcoes do modulo `random`. Assim podemos usar `choice`, que escolhe um item aleatoriamente.

Uma forma mais especifica seria `from random import choice`, mas o codigo atual usa a importacao original.

## 2. Dicionario do DNA

```python
bases = {"A": "T", "T": "A", "C": "G", "G": "C"}
```

Esse dicionario guarda os pares da fita de DNA:

- A combina com T.
- T combina com A.
- C combina com G.
- G combina com C.

Quando usamos `bases[base]`, o Python procura o par correspondente a base guardada em `base`.

Exemplo:

```python
base = "A"
par = bases[base]
```

Nesse caso, `par` recebe `"T"`.

## 3. Dicionario do RNA

```python
rnab = {"A": "U", "T": "A", "C": "G", "G": "C"}
```

Esse dicionario transforma uma base de DNA na base correspondente do RNA:

```text
A -> U
T -> A
C -> G
G -> C
```

O RNA usa `U` no lugar de `T`.

## 4. Dicionario de cores

```python
cores = {
    "A": "...A...",
    "T": "...T...",
    "C": "...C...",
    "G": "...G...",
    "=": "...=...",
    "\u2261": "...\u2261...",
    "U": "...U...",
}
```

O dicionario `cores` guarda os simbolos com codigos de cor para o terminal. Assim, cada base pode aparecer com uma cor diferente.

Por exemplo, `cores["A"]` retorna o `A` com a cor configurada.

O trecho `\033[0m` reseta a cor depois do simbolo.

## 5. Recebendo a quantidade

```python
quant = int(input("Quantidade de bases nitrogenadas: "))
```

`input()` pergunta um valor ao usuario. Como o resultado do `input()` e texto, `int()` transforma esse texto em um numero inteiro.

Se o usuario digitar `5`, o programa guarda:

```python
quant = 5
```

## 6. Criando a fita de DNA

```python
fita_dna = []
```

Cria uma lista vazia para guardar todas as bases sorteadas.

Essa lista e necessaria porque o RNA sera criado depois. Se as bases nao fossem guardadas, o programa teria apenas a ultima base na variavel `base` quando o primeiro laco terminasse.

A ideia geral e:

```text
sortear -> guardar -> usar depois
```

## 7. Repetindo a geracao

```python
for i in range(quant):
```

Repete o bloco `quant` vezes.

Se `quant` for 5, o bloco sera executado 5 vezes. A variavel `i` conta as repeticoes, embora nao seja usada diretamente no codigo.

Quando o numero da repeticao nao for necessario, tambem seria possivel usar `_` no lugar de `i`.

## 8. Sorteando e guardando uma base

```python
base = choice(list(bases.keys()))
```

A expressao `bases.keys()` pega as chaves do dicionario:

```text
A, T, C, G
```

`list(bases.keys())` transforma essas chaves em uma lista:

```python
["A", "T", "C", "G"]
```

`choice(...)` escolhe uma dessas bases aleatoriamente e guarda o resultado na variavel `base`.

```python
fita_dna.append(base)
```

`append()` adiciona a base escolhida ao final da lista `fita_dna`.

Por exemplo, depois de alguns sorteios, a lista pode ficar assim:

```python
fita_dna = ["A", "C", "T", "G"]
```

## 9. Encontrando o par do DNA

```python
par = bases[base]
```

Usa a base sorteada para encontrar a base complementar do DNA.

Se `base` for `"C"`, o dicionario retorna `"G"`.

## 10. Escolhendo a ponte

```python
if base in ["A", "T"]:
    ponte = "="
else:
    ponte = "\u2261"
```

Verifica qual tipo de ponte deve ser usado na representacao:

- A e T usam `=`.
- C e G usam `\u2261`.

A estrutura `if/else` significa: se a condicao for verdadeira, execute o primeiro bloco; caso contrario, execute o bloco do `else`.

## 11. Mostrando a fita de DNA

```python
print(f"| {cores[base]} {cores[ponte]} {cores[par]} |")
```

O `f` antes das aspas permite colocar variaveis dentro do texto.

O resultado fica parecido com:

```text
| A = T |
| C \u2261 G |
```

As consultas `cores[base]`, `cores[ponte]` e `cores[par]` aplicam as cores corretas.

## 12. Perguntando se o RNA deve ser mostrado

```python
resposta = input("Deseja ver o RNA? s/n: ").lower()
```

Pergunta ao usuario se ele deseja ver o RNA.

O metodo `.lower()` transforma a resposta em letras minusculas. Assim, tanto `S` quanto `s` se tornam `s`.

```python
if resposta == "s":
```

O bloco do RNA so sera executado se a resposta for `s`.

A pergunta acontece depois do DNA porque primeiro o programa precisa terminar de gerar e mostrar a fita original.

## 13. Montando a fita de RNA

```python
fita_rna = ""
```

Cria uma string vazia para acumular as bases de RNA.

```python
for base in fita_dna:
```

Percorre cada base que foi guardada na fita original de DNA.

Essa linha e essencial: o RNA usa a fita que ja foi sorteada. Ele nao faz um novo sorteio.

```python
rna = rnab[base]
```

Busca no dicionario `rnab` a base de RNA correspondente.

Por exemplo:

```python
base = "A"
rna = rnab[base]
```

Resultado:

```python
rna = "U"
```

```python
fita_rna += rna
```

Adiciona a base de RNA na sequencia.

Isso equivale a:

```python
fita_rna = fita_rna + rna
```

Se as bases convertidas forem `U`, `G`, `A`, a string terminara como:

```python
fita_rna = "UGA"
```

## 14. Mostrando DNA e RNA juntos

```python
print("Fita de RNA:")
```

Mostra um titulo antes da fita de RNA.

```python
for base in fita_dna:
```

Percorre novamente cada base original do DNA. Fazer esse novo laco permite mostrar a base do DNA junto com o seu RNA correspondente.

```python
rna = rnab[base]
```

Encontra novamente a base de RNA correspondente aquela base do DNA.

```python
if base in ["A", "T"]:
    ponte = "="
else:
    ponte = "\u2261"
```

Escolhe a ponte visual de acordo com a base do DNA.

```python
print(f"| {cores[base]} {cores[ponte]} {cores[rna]} |")
```

Mostra a base do DNA e a base correspondente do RNA na mesma linha.

O resultado fica parecido com:

```text
Fita de RNA:
| A = U |
| C \u2261 G |
| T = A |
```

## 15. Por que nao sortear o RNA novamente?

O RNA precisa ser criado a partir da fita de DNA original. Por isso, o codigo usa:

```python
for base in fita_dna:
```

Se fosse usado novamente:

```python
base = choice(list(bases.keys()))
```

o programa criaria uma base nova e aleatoria. Essa nova base poderia nao ter relacao com o DNA que ja foi mostrado.

## 16. Receita para problemas parecidos

Quando precisar gerar algo e usar o resultado depois, siga esta ordem:

1. Crie uma lista vazia.
2. Gere ou receba um valor.
3. Guarde o valor com `append()`.
4. Termine a primeira tarefa.
5. Percorra a lista guardada.
6. Transforme cada item.
7. Mostre o novo resultado.

Neste programa:

```text
base sorteada -> fita_dna -> conversao -> fita_rna
```

Essa separacao evita perder os dados originais e permite criar o RNA corretamente.
