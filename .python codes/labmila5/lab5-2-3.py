# Entrada de dados
hora_prova = int(input("Hora de início da prova (0-23): "))
minuto_prova = int(input("Minuto de início da prova (0-59): "))
hora_chegada = int(input("Hora de chegada do(a) estudante (0-23): "))
minuto_chegada = int(input("Minuto de chegada do(a) estudante (0-59): "))
minutos_prova = hora_prova * 60 + minuto_prova
minutos_chegada = hora_chegada * 60 + minuto_chegada
diferenca = minutos_prova - minutos_chegada
if diferenca < 0:
    print("Tarde demais: Chegou depois do horário da prova.")
elif diferenca > 30:
    print("Cedo demais: Chegou mais de 30 minutos antes da prova.")
else:
    print("Chegou no horário: Chegou no horário da prova ou até 30 minutos antes.")