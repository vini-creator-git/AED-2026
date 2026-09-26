etp1 = int(input("Qual a nota na primeira etapa?"))
etp2 = int(input("Qual a nota na segunda etapa?"))
etp3 = int(input("Qual a nota na terceira etapa?"))
total = etp1 + etp2 + etp3
print(total >= 60 and etp1 > 0 and etp2 > 0 and etp3 > 0)