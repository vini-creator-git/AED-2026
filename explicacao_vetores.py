# arquivo criado para estudo independente de conceitos vetoriais


from array import array


# 1. Criando um vetor (lista)
notas = [8.5, 7.0, 9.5, 6.0]
print("Vetor de notas:", notas)


# 2. len() mostra a quantidade de elementos do vetor
quantidade_notas = len(notas)
print("Quantidade de notas:", quantidade_notas)


# 3. sum() soma todos os valores numericos do vetor
soma_notas = sum(notas)
print("Soma das notas:", soma_notas)


# 4. A media pode ser calculada usando sum() e len()
media_notas = sum(notas) / len(notas)
print("Media das notas:", media_notas)


# 5. O indice indica a posicao de um elemento.
# A primeira posicao e 0, a segunda e 1, e assim por diante.
print("Primeira nota:", notas[0])
print("Segunda nota:", notas[1])
print("Ultima nota:", notas[-1])


# 6. Alterando um elemento do vetor
notas[0] = 9.0
print("Vetor depois da alteracao:", notas)


# 7. Adicionando elementos
notas.append(10.0)  # adiciona no final
notas.insert(1, 8.0)  # adiciona na posicao escolhida
print("Vetor depois de adicionar elementos:", notas)


# 8. Removendo elementos
notas.remove(6.0)  # remove o primeiro valor igual a 6.0
ultima_nota = notas.pop()  # remove e devolve o ultimo elemento
print("Nota removida com pop:", ultima_nota)
print("Vetor depois das remocoes:", notas)


# 9. Percorrendo o vetor com for
print("Notas do vetor:")
for nota in notas:
    print(nota)


# 10. Encontrando maior e menor valor
print("Maior nota:", max(notas))
print("Menor nota:", min(notas))


# 11. Fatiamento: copia uma parte do vetor
primeiras_notas = notas[0:3]
print("Tres primeiras notas:", primeiras_notas)


# 12. Array tipado
# Diferente da lista, o array armazena valores de um unico tipo.
unidades = array("i", [10, 20, 30, 40])
print("Array de inteiros:", unidades)
print("Soma do array:", sum(unidades))
print("Quantidade de elementos no array:", len(unidades))
