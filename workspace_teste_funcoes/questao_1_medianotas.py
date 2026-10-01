#entrada de dados
nomes = []
notas = []
for i in range(10):
    nomes.append(input(f"Nome {i+1}: "))
    notas.append(float(input(f"Nota {i+1}: ")))
print(nomes, notas)
#q2
from func import medianotas

notas = []
for i in range(10):

    notas.append(float(input(f"Nota {i+1}: ")))

print(f"Média: {medianotas(notas):.2f}")
#q3
from func import medianotas, acima_media

notas = []
for i in range(10):
    notas.append(float(input(f"Nota {i+1}: ")))

media = medianotas(notas)
#q4
from func import separarnotas

notas = []
for i in range(10):
    notas.append(float(input(f"Nota {i+1}: ")))

pares, impares = separarnotas(notas)
print(f"Índice par: {pares}")
print(f"Índice ímpar: {impares}")
#q5
from func import estatisticas

notas = []
for i in range(10):
    notas.append(float(input(f"Nota {i+1}: ")))

aprov, rec, reprov = estatisticas(notas)
print(f"Aprovados: {aprov:.1f}% | Recuperação: {rec:.1f}% | Reprovados: {reprov:.1f}%")
#q6
from func import maiornota

nomes = []
notas = []
for i in range(10):
    nomes.append(input(f"Nome {i+1}: "))
    notas.append(float(input(f"Nota do {nomes[i]}: ")))

maior, aluno = maiornota(notas, nomes)
print(f"Maior nota: {aluno} com {maior}")
#q7
from func import conceitos

notas = []
for i in range(10):
    notas.append(float(input(f"Nota {i+1}: ")))

print(f"Conceitos: {conceitos(notas)}")