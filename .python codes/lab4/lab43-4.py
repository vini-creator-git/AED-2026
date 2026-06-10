#ae * 2 cd série * 5 e total * nivel de intensidade -> se tudo >= 100 -> true
aeróbico = int(input("Quantos minutos de aeróbicos vc fez?"))
serie = int(input("Quantas series vc fez?"))
intensidade = int(input("Qual o nivel de intensidade? (1/2/3)"))
total = aeróbico * 2 + serie*5 
total2 = total * intensidade
print(total2 >= 100)