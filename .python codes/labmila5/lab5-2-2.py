import random
jogada_pc = random.choice (["pedra","papel",'tesoura'])
player=input("Pedra papel ou tesoura?")
p1='player wins'
c2='pc wins'
e3=('empate')
print ("jogada do pc foi: " , jogada_pc)
if player=="pedra" and jogada_pc== "tesoura":
    print (p1)
elif player=='tesoura'and jogada_pc=='pedra':
    print (c2)
elif player=='papel' and jogada_pc=='pedra':
    print(p1)
elif player=='pedra' and jogada_pc=='papel':
    print(c2)
elif player=='pedra' and jogada_pc=='pedra':
    print(e3)
elif player=='papel' and jogada_pc=='papel':
    print(e3)
elif player=='tesoura' and jogada_pc=='tesoura':
    print(e3)
elif player=='tesoura' and jogada_pc=='papel':
    print(p1)
elif player=='papel' and jogada_pc=='tesoura':
    print(c2)
else :
    print('insira uma entrada valida')