#Faça um programa parecido com a questão anterior, 
# mas agora você não vai apenas contar os valores que o usuário digitar, 
# mas também tirar a média. Ou seja, você deve somar os valores que o usuário forneceu 
# e ao final dividir pelo contador de valores digitados.
usr=1
contador=0
soma = 0
while usr !=0:
    usr=int(input('digite um valor'))
    contador+=1
    soma+=usr

print(soma/contador)