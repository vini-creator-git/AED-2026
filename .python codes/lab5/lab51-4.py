dis=int(input("Qual a distância da entrega em km?:"))
peso= float(input("Qual o peso do pacote em quilogramas:?"))
if dis <= 100 and peso < 10:
    print(f"O total de frete a se pagar é {peso}")
elif dis <= 100 and peso >= 10:
    print(f"O total de frete a se pagar é {peso + 10}")
elif dis >=101 and dis <= 300 and peso < 10:
    print(f"O total de frete a se pagar é {peso*1.5}")
elif peso>10 and dis <=300 and dis >= 101:
    print(f"O total de frete a se pagar é {peso*1.5+10}")
elif dis > 300 and peso >= 10:
    print(f"O total de frete a se pagar é {peso*2 + 10}")
elif dis > 300 and peso < 10:
    print(f"O total de frete a se pagar é {peso*2}")