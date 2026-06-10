idade = int(input("Qual a sua idade?"))
qts_jgs = int(input("Quantos jogos já jogou?"))
qts_venceu = int(input("Quantos venceu?"))
idd = idade >= 14 and idade <= 18
porcento = qts_venceu >= (qts_jgs*0.4)
jogou = qts_jgs >= 3
print(idd and porcento and jogou)
