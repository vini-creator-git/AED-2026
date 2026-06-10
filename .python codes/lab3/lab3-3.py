salario_hora = 20
horas_semana = 40
salario_bruto = salario_hora * horas_semana
inss = salario_bruto * 0.10
sindicato = salario_bruto * 0.05
salario_liquido = salario_bruto - inss - sindicato
print(f"Seu salário bruto é de R${salario_bruto}")
print(f"O INSS desconta R${inss:.2f} por semana")
print(f"O sindicato desconta R${sindicato:.2f} por semana")
print(f"Seu salário líquido é de R${salario_liquido:.2f}")