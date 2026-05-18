#Vamos dificultar um pouco colocando ifs dentro do while. 
# Escreva um programa que lê 10 valores do usuário 
# e conta apenas a quantidade de valores positivos digitados.
usr=1
contador=0

while contador<10 :
    usr=int(input('digite um valor'))
    contador+=1
    if usr<0:
        contador==contador+usr




print(contador)