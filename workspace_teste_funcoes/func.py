def medianotas(notas):
    soma = 0
    for i in range(len(notas)):
        soma += notas[i]
    return soma / len(notas)

def acima_media(notas, media):
    cont = 0
    for nota in notas:
        if nota >= media:
            cont += 1
    return cont

def separarnotas(notas):
    pares = []
    impares = []
    for i in range(len(notas)):
        if i % 2 == 0:
            pares.append(notas[i])
        else:
            impares.append(notas[i])
    return pares, impares

def estatisticas(notas):
    aprovados = 0
    recuperacao = 0
    reprovados = 0
    for nota in notas:
        if nota >= 7:
            aprovados += 1
        elif nota >= 5: # de 5 a 6.9
            recuperacao += 1
        else: # menor que 5
            reprovados += 1

    total = len(notas)
    perc_aprov = (aprovados / total) * 100
    perc_rec = (recuperacao / total) * 100
    perc_rep = (reprovados / total) * 100

    return perc_aprov, perc_rec, perc_rep

def maiornota(notas, nomes):
    maior = notas[0]
    aluno_maior = nomes[0]
    for i in range(1, len(notas)):
        if notas[i] > maior:
            maior = notas[i]
            aluno_maior = nomes[i]
    return maior, aluno_maior

def conceitos(notas):
    conceitos_lista = []
    for nota in notas:
        if nota >= 9:
            conceitos_lista.append('A')
        elif nota >= 7:
            conceitos_lista.append('B')
        elif nota >= 5:
            conceitos_lista.append('C')
        else:
            conceitos_lista.append('D')
    return conceitos_lista