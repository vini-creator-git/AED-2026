print("Bem vindo ao sistema de validador de aposentadoria")
genero = input("Escolha seu gênero (M ou F): ")
idade = int(input("Sua idade: "))
tempo_servico = int(input("Tempo de serviço (em anos): "))

pode_aposentar = (genero == "F" and idade > 60) or (genero == "M" and idade >= 65) or (tempo_servico >= 30) or (idade >= 60 and tempo_servico >= 25)

print(pode_aposentar)
