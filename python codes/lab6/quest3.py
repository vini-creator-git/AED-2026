#Um dos principais usos do laço com while é fazer operações com quantidades de valores desconhecidas. 
# Nesse exercício você lerá inúmeros valores inteiros do usuário até que ele digite o valor zero. 
# Seu trabalho é contar quantos valores o usuário digitou e imprimir ao final.
usr=1
contador=0
while usr !=0:
    usr=int(input('digite um valor'))
    contador+=1
print(contador)
