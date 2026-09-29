import funcao


vet=[0,0,0,0,0,0,0,0,0,0]

for x in range(0,10):
    vet[x] = int(input(f"digite um valor para a posição {x+1}: "))
print(f"o maior valor do vetor é: {funcao.buscamaior(vet)}")