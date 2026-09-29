import pratica as pr
#"Ana", "Bruno", "Carla", "Diego", "Eduardo", "Fernanda", "Gustavo", "Helena", "Igor", "Juliana"
#8.5, 7.0, 9.5, 6.0, 8.0, 7.5, 9.0, 6.5, 8.0, 7.0

notas = []
alunos = []
print("Seja bem-vindo ao sistema de notas!")
for i in range(10):
    nota = float(input("Digite a nota no formato numero.decimal: "))
    notas.append(nota)
    aluno = input("Digite o nome do aluno: ")
    alunos.append(aluno)

print()
print(" alunos:", alunos)
print("notas:", notas)

media = pr.media_notas(notas)
print()
print(f"A média das notas é: {media}")

print()
for aluno, nota in zip(alunos, notas):
    pr.mediaal(aluno, nota)

print()
posic = pr.separar_notas_por_posicao(notas)
print(f"Notas  das posições pares e ímpares, respectivamente: {posic}")

print()
estat = pr.estatnotas(notas)
print(estat)

print()
maior = pr.maiornota(notas, alunos)
print(maior)

print()
conc = pr.conceito(notas)
print(f"Notas separadas por conceitos (A, B, C e D): {conc}")