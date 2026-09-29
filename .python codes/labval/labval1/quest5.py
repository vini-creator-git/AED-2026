bddenum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

procuraae = int(input("Digite um número para procurar no vetor: "))

num = bddenum[0:10]

encontrado = False

for item in num:
    if procuraae == item:
        encontrado = True

if encontrado:
    print(f"O número {procuraae} foi encontrado no vetor.")
else:
    print(f"O número {procuraae} não foi encontrado no vetor.")
