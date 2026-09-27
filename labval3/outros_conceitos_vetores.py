



# arquivo criado para estudo independente de conceitos vetoriais

# 1. enumerate() fornece o indice e o valor ao mesmo tempo.
produtos = ["caderno", "caneta", "borracha"]
print("Produtos cadastrados:")
for indice, produto in enumerate(produtos):
    print(indice, produto)


# 2. in verifica se um valor esta dentro do vetor.
produto_procurado = "caneta"
if produto_procurado in produtos:
    print("Produto encontrado:", produto_procurado)
else:
    print("Produto nao encontrado")


# 3. index() informa a posicao da primeira ocorrencia de um valor.
posicao_borracha = produtos.index("borracha")
print("Posicao da borracha:", posicao_borracha)


# 4. sorted() cria uma nova versao ordenada do vetor.
idades = [22, 18, 35, 21, 19]
idades_ordenadas = sorted(idades)
idades_decrescentes = sorted(idades, reverse=True)
print("Idades originais:", idades)
print("Idades em ordem crescente:", idades_ordenadas)
print("Idades em ordem decrescente:", idades_decrescentes)


# 5. sort() ordena o proprio vetor e nao cria outro.
idades.sort()
print("Vetor depois do sort():", idades)


# 6. zip() junta elementos de dois vetores relacionados.
alunos = ["Ana", "Bruno", "Carla"]
notas = [8.5, 7.0, 9.5]
print("Alunos e suas notas:")
for aluno, nota in zip(alunos, notas):
    print(aluno, "-", nota)


# 7. Compreensao de listas cria um novo vetor de forma resumida.
numeros = [1, 2, 3, 4, 5, 6]
dobros = [numero * 2 for numero in numeros]
print("Dobro dos numeros:", dobros)


# 8. Compreensao com condicao filtra os elementos.
pares = [numero for numero in numeros if numero % 2 == 0]
print("Numeros pares:", pares)


# 9. any() verifica se pelo menos um elemento atende a uma condicao.
notas_baixas = [4.0, 7.5, 8.0, 6.5]
existe_nota_baixa = any(nota < 5 for nota in notas_baixas)
print("Existe nota abaixo de 5?", existe_nota_baixa)


# 10. all() verifica se todos os elementos atendem a uma condicao.
todos_aprovados = all(nota >= 6 for nota in notas_baixas)
print("Todos foram aprovados?", todos_aprovados)


# 11. copy() cria uma copia independente do vetor.
vetor_original = [10, 20, 30]
vetor_copia = vetor_original.copy()
vetor_copia.append(40)
print("Vetor original:", vetor_original)
print("Vetor copia alterado:", vetor_copia)


# 12. A funcao sum() tambem pode somar valores filtrados.
notas_aprovadas = [nota for nota in notas_baixas if nota >= 6]
media_aprovados = sum(notas_aprovadas) / len(notas_aprovadas)
print("Media das notas aprovadas:", media_aprovados)
