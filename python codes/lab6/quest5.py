#Vamos dificultar um pouco colocando ifs dentro do while. 
# Escreva um programa que lê 10 valores do usuário 
# e conta apenas a quantidade de valores positivos digitados.
usr=1
contador=0
while usr > 0 :
    usr=int(input('digite dez valores'))
    contador+=1 and contador>0
    if contador>10:
        print('digite apenas 10 digitos')
    else:
        print(contador)
print("fim")