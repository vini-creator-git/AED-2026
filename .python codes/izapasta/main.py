#entrada de dados
nomes = []
notas = []
for indice in range(10):
    nomes.append(input(f"Nome {indice + 1}: "))
    notas.append(float(input(f"Nota {indice + 1}: ")))
print(nomes, notas)
#q2
from func import acima_media, conceitos, estatisticas, maiornota, medianotas, separarnotas

print(f"Média: {medianotas(notas):.2f}")
#q3
media = medianotas(notas)
print(f"Notas acima da média: {acima_media(notas, media)}")
#q4
pares, impares = separarnotas(notas)
print(f"Índice par: {pares}")
print(f"Índice ímpar: {impares}")
#q5
aprov, rec, reprov = estatisticas(notas)
print(f"Aprovados: {aprov:.1f}% | Recuperação: {rec:.1f}% | Reprovados: {reprov:.1f}%")
#q6
maior, aluno = maiornota(notas, nomes)
print(f"Maior nota: {aluno} com {maior}")
#q7
print(f"Conceitos: {conceitos(notas)}")