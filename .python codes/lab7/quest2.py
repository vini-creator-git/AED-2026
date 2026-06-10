#a) Contar quantos números ímpares o usuário digitou. 
# o numero do contador nunca sobe por isso o while fica infinito

N = int(input("Quantos números quer digitar?"))
contador = 1
impares = 0

while contador <= N:
    num = int(input("Digite um número: "))
    if num % 2 != 0: 
        impares += 1
    contador+=1
print(f"Quantidade de ímpares: {impares}")
