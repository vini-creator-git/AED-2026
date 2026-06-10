valor_hora = float(input("Quanto você recebe por hora? "))
horas_trabalhadas = float(input("Quantas horas trabalha por semana? "))
bruto = valor_hora * horas_trabalhadas
liquido = bruto - (bruto * 0.10) - (bruto * 0.05)

print(f"Seu salário bruto é de R${bruto:.2f}")
print(f"Seu salário líquido é de R${liquido:.2f}")
