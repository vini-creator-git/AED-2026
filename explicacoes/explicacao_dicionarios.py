"""Guia pratico dos principais conceitos de dicionarios em Python."""

# Um dicionario guarda dados no formato chave: valor.
aluno = {
    "nome": "Ana",
    "idade": 20,
    "notas": [8.5, 7.0, 9.0],
}
print("Dicionario inicial:", aluno)

# As chaves devem ser unicas e imutaveis, como str, int ou tuple.
# Os valores podem ser de qualquer tipo e podem se repetir.
print("Nome:", aluno["nome"])
print("Nota que nao existe:", aluno.get("media", "Ainda nao calculada"))

# Adicionar uma chave nova e alterar uma chave existente.
aluno["curso"] = "AED"
aluno["idade"] = 21
print("Depois de adicionar e alterar:", aluno)

# update() adiciona ou altera varias chaves de uma vez.
aluno.update({"periodo": 2, "ativo": True})
print("Depois de update:", aluno)

# setdefault() cria a chave somente se ela ainda nao existir.
aluno.setdefault("cidade", "Belo Horizonte")
aluno.setdefault("nome", "Outro nome")
print("Depois de setdefault:", aluno)

# Testar se uma chave existe. O operador in verifica chaves, nao valores.
print("nome" in aluno)
print("Ana" in aluno)
print("Ana" in aluno.values())

# Percorrer chaves, valores ou pares chave-valor.
print("Chaves:")
for chave in aluno:
    print(chave)

print("Valores:")
for valor in aluno.values():
    print(valor)

print("Pares:")
for chave, valor in aluno.items():
    print(chave, "=", valor)

# Quantidade de elementos.
print("Quantidade de chaves:", len(aluno))

# Remover elementos.
curso = aluno.pop("curso")
print("Valor removido com pop:", curso)
ultimo_par = aluno.popitem()
print("Ultimo par removido com popitem:", ultimo_par)

# del remove uma chave conhecida. clear() remove tudo.
del aluno["ativo"]
print("Depois de del:", aluno)

copia = aluno.copy()
copia.clear()
print("Copia limpa:", copia)
print("Original preservado:", aluno)

# Cuidado: uma atribuicao nao cria uma copia independente.
referencia = aluno
referencia["novo"] = "alteracao no original"
print("Original apos alterar referencia:", aluno)
del aluno["novo"]

# Dicionarios podem ficar aninhados.
turma = {
    "aluno1": {"nome": "Ana", "nota": 8.5},
    "aluno2": {"nome": "Bruno", "nota": 7.0},
}
print("Nota de Ana:", turma["aluno1"]["nota"])

# Compreensao de dicionario: cria um dicionario de forma concisa.
quadrados = {numero: numero ** 2 for numero in range(1, 6)}
pares = {numero: numero ** 2 for numero in range(1, 6) if numero % 2 == 0}
print("Quadrados:", quadrados)
print("Quadrados dos pares:", pares)

# Inverter chaves e valores funciona quando os valores tambem sao unicos e imutaveis.
original = {"A": "T", "C": "G"}
invertido = {valor: chave for chave, valor in original.items()}
print("Dicionario invertido:", invertido)

# Um dicionario pode contar ocorrencias.
letras = "banana"
contagem = {}
for letra in letras:
    contagem[letra] = contagem.get(letra, 0) + 1
print("Contagem de letras:", contagem)

# Comparacao: a ordem dos pares nao e o objetivo principal de um dicionario.
print({"a": 1, "b": 2} == {"b": 2, "a": 1})

# Chaves imutaveis funcionam; listas nao podem ser chaves.
coordenadas = {(0, 0): "origem", (1, 2): "ponto"}
print("Valor da coordenada:", coordenadas[(1, 2)])

# Para salvar ou carregar dicionarios em arquivos, json e uma opcao comum:
# import json
# texto = json.dumps(aluno, ensure_ascii=False, indent=2)
# dados = json.loads(texto)

# Resumo dos metodos mais usados:
# get, keys, values, items, update, setdefault, pop, popitem, clear e copy.
