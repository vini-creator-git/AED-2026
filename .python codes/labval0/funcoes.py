def fatorial(numero):
    resultado = 1 
    for i in range(1, numero + 1): 
        resultado *= i 
        return resultado

def reajuste_salarial(salario, percentual): 
    novo_salario = salario + (salario * percentual / 100) 
    return novo_salario

def celsius_para_fahrenheit(celsius): 
    fahrenheit = (celsius * 9 / 5) + 32 
    return fahrenheit   

def fahrenheit_para_celsius(fahrenheit): 
    celsius = (fahrenheit - 32) * 5 / 9 
    return celsius

def media_notas(nota1, nota2, nota3):
    media = (nota1 + nota2 + nota3) / 3 
    return media

def area_circulo(raio): 
    pi = 3.14159 
    area = pi * (raio ** 2) 
    return area
