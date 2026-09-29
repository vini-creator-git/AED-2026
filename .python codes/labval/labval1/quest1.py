#! somar os elementos pares e impares de um vetor
vetor = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
soma_pares = 0
soma_impares = 0

for elemento in vetor:
    if elemento % 2 == 0:
        soma_pares += elemento
    else:
        soma_impares += elemento

print(f"Soma dos elementos pares: {soma_pares}")
print(f"Soma dos elementos ímpares: {soma_impares}")