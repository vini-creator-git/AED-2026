valor = int(input())

nota_100 = valor // 100
valor %= 100

nota_50 = valor // 50
valor %= 50

nota_20 = valor // 20
valor %= 20

nota_10 = valor // 10
valor %= 10

nota_5 = valor // 5
valor %= 5

nota_2 = valor // 2
valor %= 2

nota_1 = valor

print(f"{nota_100} nota(s) de 100,00")
print(f"{nota_50} nota(s) de 50,00")
print(f"{nota_20} nota(s) de 20,00")
print(f"{nota_10} nota(s) de 10,00")
print(f"{nota_5} nota(s) de 5,00")
print(f"{nota_2} nota(s) de 2,00")
print(f"{nota_1} nota(s) de 1,00")