vitorias=0

empates=0

derrotas=0

n=int(input('quantos jogos foram jogados'))
for i in range(1,n+1):
    galo=int(input ( 'quantos gols o galo fez? '))
    adv=int(input('quantos gols o time adversario fez? '))
    if galo>adv:
        vitorias+=1
    
    elif galo==adv:
        empates+=1
    
    elif galo<adv:
        derrotas+=1
    pontosgeral=vitorias*3+empates
print(f'o galo ganhou {vitorias} jogos perdeu {derrotas} e empatou {empates}  no final do campeonato o galo ficou com {pontosgeral} pontos ')
