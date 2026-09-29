# multiplicacao dos elementos com valores entre 20 e 60 incluindo eles
vetor = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # cria uma lista de numeros
resultado = 1  # inicia o resultado com 1 para fazer a multiplicacao
for elemento in vetor:  # passa por cada elemento da lista
    if 20 <= elemento <= 60:  # verifica se o elemento esta entre 20 e 60
        resultado *= elemento  # multiplica o resultado pelo elemento selecionado

print(f"O resultado da multiplicação dos elementos entre 20 e 60 é: {resultado}")  # mostra o resultado na tela