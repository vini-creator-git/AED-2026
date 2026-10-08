"""Guia pratico da notacao com ponto em Python.

A notacao objeto.metodo() significa: execute um metodo pertencente ao objeto.
Este arquivo pode ser lido como material de estudo e tambem pode ser executado.
"""


# ============================================================
# 1. O que significa usar um ponto?
# ============================================================

# O ponto acessa algo que pertence a um objeto:
# - um metodo: objeto.metodo()
# - um atributo: objeto.atributo
# - uma funcao ou constante de um modulo: modulo.funcao()

nome = "  Ana Silva  "

# strip() e um metodo de str.
# Ele remove espacos, quebras de linha e tabulacoes das extremidades.
# Nao remove espacos do meio e nao altera a string original.
nome_sem_espacos = nome.strip()
print("strip():", repr(nome_sem_espacos))

# lower() transforma todas as letras em minusculas.
# Tambem devolve uma nova string, sem alterar a string original.
nome_minusculo = nome_sem_espacos.lower()
print("lower():", nome_minusculo)

# Os metodos podem ser encadeados: o resultado de um e usado pelo proximo.
nome_padronizado = nome.strip().lower()
print("strip().lower():", nome_padronizado)

# upper(), title() e capitalize() tambem sao metodos de strings.
print("upper():", nome_padronizado.upper())
print("title():", nome_padronizado.title())
print("capitalize():", nome_padronizado.capitalize())


# ============================================================
# 2. Metodos de strings (str)
# ============================================================

texto = "  Python e muito bom  "

# Remover apenas caracteres especificos das extremidades:
# strip("xyz") remove qualquer x, y ou z do inicio e do fim.
codigo = "###AED###"
print("strip com caracteres:", codigo.strip("#"))

# lstrip() remove somente da esquerda; rstrip(), somente da direita.
print("lstrip():", repr(texto.lstrip()))
print("rstrip():", repr(texto.rstrip()))

# split() divide uma string e cria uma lista.
frase = "Python;Java;C"
linguagens = frase.split(";")
print("split():", linguagens)

# join() pertence a uma string separadora e junta elementos de uma lista.
print("join():", " - ".join(linguagens))

# replace() troca uma parte por outra.
print("replace():", texto.replace("bom", "util"))

# find() devolve a posicao da primeira ocorrencia, ou -1 se nao encontrar.
print("find():", texto.find("Python"))

# count() conta ocorrencias.
print("count():", texto.count("o"))

# startswith() e endswith() verificam inicio e fim.
print("startswith():", texto.strip().startswith("Python"))
print("endswith():", texto.strip().endswith("bom"))

# isdigit(), isalpha() e isalnum() verificam o conteudo.
print("isdigit():", "123".isdigit())
print("isalpha():", "abc".isalpha())
print("isalnum():", "abc123".isalnum())

# Comparacao ignorando maiusculas e espacos:
resposta = "  SIM  "
print(resposta.strip().lower() == "sim")


# ============================================================
# 3. Metodos de listas (list)
# ============================================================

notas = [8.0, 6.5, 9.0]

# append() adiciona um elemento no final.
notas.append(7.5)

# insert() adiciona em uma posicao.
notas.insert(1, 10.0)

# extend() adiciona varios elementos.
notas.extend([5.0, 8.5])
print("Lista depois de append, insert e extend:", notas)

# remove() remove a primeira ocorrencia do valor.
notas.remove(5.0)

# pop() remove e devolve um elemento. Sem indice, remove o ultimo.
ultima_nota = notas.pop()
print("Elemento devolvido por pop():", ultima_nota)

# index() mostra a posicao de um valor; count() conta ocorrencias.
print("index():", notas.index(10.0))
print("count():", notas.count(8.0))

# sort() ordena a propria lista; sorted() e uma funcao que cria outra lista.
notas.sort()
print("sort():", notas)
notas.reverse()
print("reverse():", notas)

# copy() cria uma copia rasa da lista.
copia_notas = notas.copy()
print("copy():", copia_notas)

# clear() remove todos os elementos da lista.
copia_notas.clear()
print("clear():", copia_notas)


# ============================================================
# 4. Metodos de dicionarios (dict)
# ============================================================

aluno = {"nome": "Ana", "idade": 20}

# get() acessa uma chave sem gerar erro quando ela nao existe.
print("get():", aluno.get("curso", "Nao informado"))

# keys(), values() e items() devolvem visoes do dicionario.
print("keys():", aluno.keys())
print("values():", aluno.values())
print("items():", aluno.items())

# update() adiciona ou altera varias chaves.
aluno.update({"curso": "AED", "idade": 21})

# setdefault() cria a chave somente se ela ainda nao existir.
aluno.setdefault("cidade", "Belo Horizonte")

# pop() remove uma chave e devolve o valor removido.
curso = aluno.pop("curso")
print("pop():", curso)

# copy() copia o dicionario e clear() o esvazia.
copia_aluno = aluno.copy()
copia_aluno.clear()
print("Dicionario original:", aluno)
print("Copia depois de clear():", copia_aluno)


# ============================================================
# 5. Metodos de conjuntos (set)
# ============================================================

bases = {"A", "C", "G"}

# add() adiciona um elemento; elementos repetidos sao ignorados.
bases.add("T")

# discard() remove sem gerar erro se o elemento nao existir.
bases.discard("X")

# union(), intersection() e difference() fazem operacoes de conjuntos.
outras_bases = {"A", "T"}
print("union():", bases.union(outras_bases))
print("intersection():", bases.intersection(outras_bases))
print("difference():", bases.difference(outras_bases))


# ============================================================
# 6. Arquivos e modulos tambem usam ponto
# ============================================================

# Um arquivo aberto possui metodos como write(), read() e close().
# O bloco with fecha o arquivo automaticamente ao terminar.
with open("explicacao_ponto_exemplo.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write("Exemplo de escrita em arquivo.\n")

with open("explicacao_ponto_exemplo.txt", "r", encoding="utf-8") as arquivo:
    conteudo = arquivo.read()
    print("read():", conteudo.strip())

# O ponto tambem acessa funcoes dentro de modulos.
import math

print("math.sqrt():", math.sqrt(16))
print("math.pi:", math.pi)


# ============================================================
# 7. Atributos e metodos de classes
# ============================================================


class Aluno:
    def __init__(self, nome, nota):
        self.nome = nome       # atributo do objeto
        self.nota = nota       # outro atributo do objeto

    def aprovado(self):
        return self.nota >= 7


estudante = Aluno("Ana", 8.5)
print("Atributo com ponto:", estudante.nome)
print("Metodo da classe com ponto:", estudante.aprovado())


# ============================================================
# 8. Ponto nao e usado em tudo
# ============================================================

# Funcoes built-in sao chamadas diretamente:
print("len():", len(notas))
print("sum():", sum(notas))

# Operadores tambem nao usam ponto:
# +, -, *, /, ==, !=, >, <, >=, <=, and, or e not.

# Acesso por indice usa colchetes, nao ponto:
print("Primeiro elemento:", notas[0])
print("Valor do dicionario:", aluno["nome"])


# Resumo:
# objeto.metodo()       -> chama um metodo e normalmente pode alterar ou devolver algo
# objeto.atributo       -> acessa um dado pertencente ao objeto
# modulo.funcao()       -> chama uma funcao que esta dentro de um modulo
# strip()               -> remove espacos das extremidades
# lower()               -> transforma letras em minusculas
# strip().lower()       -> encadeia dois metodos
