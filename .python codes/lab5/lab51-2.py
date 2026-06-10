a = float(input("a= "))
sinal = input("Qual sinal vc deseja")
b = float(input("b= "))
if sinal == "+":
    print(a + b)
elif sinal == "-":
    print(a - b)
elif sinal == "*":
    print(a * b)
elif b == 0 and sinal == "/":
    print("Divisão por zero não permitida")
elif sinal == "/":
    print(a/b)