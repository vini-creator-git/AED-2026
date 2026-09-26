import funcoes
num = int(input("Digite um número para calcular o fatorial: ")) 
print(f"O fatorial de {num} é {fatorial(num)}") 
print("-" * 40)  


salario = float(input("Digite o salário atual: ")) 
percentual = float(input("Digite o percentual de aumento: ")) 
print(f"Novo salário com reajuste: {reajuste_salarial(salario, percentual):.2f}") 
print("-" * 40) 

temp_c = float(input("Digite a temperatura em Celsius: ")) 
print(f"{temp_c}°C equivale a {celsius_para_fahrenheit(temp_c):.2f}°F") 

temp_f = float(input("Digite a temperatura em Fahrenheit: ")) 

print(f"{temp_f}°F equivale a {fahrenheit_para_celsius(temp_f):.2f}°C") 
print("-" * 40) 

n1 = float(input("Digite a nota do aluno 1: ")) 
n2 = float(input("Digite a nota do aluno 2:") )
n3 = float(input("Digite a nota do aluno 3:" ))
print(f"A média dos três alunos é {media_notas(n1, n2, n3):.2f}") 
print("-" * 40)  
raio = float(input("Digite o raio do círculo: "))
print(f"A área do círculo é {area_circulo(raio):.2f}")