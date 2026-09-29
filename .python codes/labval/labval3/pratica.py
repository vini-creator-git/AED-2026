
def media_notas(notas):
    soma = sum(notas)
    quantidade=len(notas)
    media=soma/quantidade
    return media



def mediaal(aluno,nota):
    if nota >= 7.0:
        return print(f"O aluno {aluno} esta na media ou acima")
    else:
        return print(f"O aluno {aluno} esta abaixo da media") 


def separar_notas_por_posicao(notas):
    pares = []
    impares = []

    for indice in range(len(notas)):
        if indice % 2 == 0:
            pares.append(notas[indice])
        else:
            impares.append(notas[indice])

    return pares, impares


def estatnotas(notas):
    aprovados=0
    recuperacao=0
    reprovados=0
    for nota in notas:
        if nota>=7:
            aprovados+=1
        elif nota>=5:
            recuperacao+=1
        else:
            reprovados+=1
    total=len(notas)
    percenaprov=aprovados*100/total
    percenrec=recuperacao*100/total
    percenareprov=reprovados*100/total
    return f"percentual de aprovados{percenaprov} pencentual recuperacao {percenrec} e percentual de reprovados{percenareprov}"



def maiornota(notas,alunos):
    maior=max(notas)
    posicao=notas.index(maior)
    aluno = alunos[posicao]
    
    return f"A maior nota foi {maior} do aluno {aluno}"







def conceito(notas):
    conceitos=[]
    for nota in notas:
        if nota>=9:
            conceitos.append("a")
        elif nota>=7:
            conceitos.append("b")
        elif nota>=5:
            conceitos.append("c")
        else:
            conceitos.append("d")
    return conceitos


