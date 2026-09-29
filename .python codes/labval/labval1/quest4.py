# somar itens nas posicoes impares do  vetor sem len
vetor = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
soma_impares = 0

for item in vetor[1::2]:
	soma_impares += item

print(soma_impares)