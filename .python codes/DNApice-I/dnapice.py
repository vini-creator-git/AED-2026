from random import choice
def porcent(sequencia):
    total=len(sequencia)
    for letra in ["A","T","C","G","U"]:
        quantidade=sequencia.count(letra)
        porcentagem= quantidade/total*100
        print(f"{letra}: {porcentagem:.2f} % ")
bases = {"A": "T", "T": "A", "C": "G", "G": "C"}
rnab = {"A": "U", "T": "A", "C": "G", "G": "C"}
parr = {"T": "A", "A": "T", "G": "C", "C": "G"}


cores = {
    "A": "\033[31mA\033[0m",
    "T": "\033[35mT\033[0m",
    "C": "\033[32mC\033[0m",
    "G": "\033[36mG\033[0m",
    "=": "\033[34m=\033[0m",
    "\u2261": "\033[33m\u2261\033[0m",
    "U": "\033[35mU\033[0m",
}
#copiei e colei o cabecalho pq era mto dificil de fzr na mao, e eu n queria perder tempo com isso tmj moises
cabecalho = [
    "╔══════════════════════════════════════╗",
    "║              DNApice                 ║",
    "║       GERADOR DE DNA E RNA           ║",
    "╚══════════════════════════════════════╝",
]
#printa o cabecalho
for linha in cabecalho:
    print(linha)

quant = int(input("Quantidade de bases nitrogenadas: "))
modo_lotes = input("Deseja gerar de 10 em 10? s/n: ").lower()
fita_dna = []
#define as bases de acordo com a quantidade escolhida pelo usuario, e printa a fita de DNA
for i in range(quant):
    base = choice(list(bases.keys()))
    fita_dna.append(base)
    par = bases[base]

    if base in ["A", "T"]:
        ponte = "="
    else:
        ponte = "\u2261"

    print(f"| {cores[base]} {cores[ponte]} {cores[par]} |")
#define se o usuario quer gerar de 10 em 10, e se sim, espera o usuario apertar enter para continuar
    if modo_lotes == "s" and (i + 1) % 10 == 0 and i + 1 < quant:
        input("Pressione Enter para gerar as próximas  bases...")
porcent(fita_dna)
#opcao se deseja ver o rna ou nn e coloca as bases correspondtentes trocando o t da direita po u e printa o rna de dez em dez tbm
resposta = input("Deseja ver o RNA? s/n: ").lower()
if resposta == "s":
    fita_rna = ""
    for base in fita_dna:
        rna = rnab[base]
        fita_rna += rna

    print("Fita de RNA:")
    for base in fita_dna:
        rna = rnab[base]
        if base in ["A", "T"]:
            ponte = "="
        else:
            ponte = "\u2261"
        print(f"| {cores[base]} {cores[ponte]} {cores[rna]} |")
    porcent(fita_rna)



see_W = input("Ver wolbachia? S/N").lower()
if see_W == "s":
    wolbachia =["T", "T", "C", "T", "T", "T", "A", "A", "A", "A", "G", "T", "C", "G", "G", "C", "A", "A", "A", "T", "A", "T", "T", "T", "G", "C", "A", "T", "T", "G", "T", "G", "T", "A", "A", "T", "T"]
    modo_lotes_w = input("Deseja ver a Wolbachia de 10 em 10? s/n: ").lower()

    print("Fita do Wolbachia:")
    for i, base in enumerate(wolbachia):
        parw = parr[base]
        if base in ["A", "T"]:
            ponte = "="
        else:
            ponte = "\u2261"
        print(f"| {cores[base]} {cores[ponte]} {cores[parw]} |")
        if modo_lotes_w == "s" and (i + 1) % 10 == 0 and i + 1 < len(wolbachia):
            input("Pressione Enter para ver as próximas bases...")
    porcent(wolbachia)
    respostaw = input("Deseja ver o RNA da bacteria? s/n: ").lower()
    if respostaw == "s":
        fita_rnaw = ""
        for base in wolbachia:
            rnaw = rnab[base]
            fita_rnaw += rnaw

        print("Fita de RNA:")
        for i, base in enumerate(wolbachia):
            rna = rnab[base]
            if base in ["A", "T"]:
                ponte = "="
            else:
                ponte = "\u2261"
            print(f"| {cores[base]} {cores[ponte]} {cores[rna]} |")
            if modo_lotes_w == "s" and (i + 1) % 10 == 0 and i + 1 < len(wolbachia):
                input("Pressione Enter para ver as próximas bases...")
        print("Sequência de RNA:", fita_rnaw)
    porcent(fita_rnaw)



dessjo=input("Deseja digitar uma sequencia especifica? s/n  ").lower()

if dessjo=="s":
    basess = input("Digite as bases: ").upper()
    lista_espec = list(basess)
    modo_lotes_espec = input("Deseja ver a sequência de 10 em 10? s/n: ").lower()

    print("Fita da sequência específica:")
    for i, base in enumerate(lista_espec):
        pare = parr[base]
        if base in ["A", "T"]:
            ponte = "="
        else:
            ponte = "\u2261"
        print(f"| {cores[base]} {cores[ponte]} {cores[pare]} |")
        if modo_lotes_espec == "s" and (i + 1) % 10 == 0 and i + 1 < len(lista_espec):
            input("Pressione Enter para ver as próximas bases...")
    porcent(lista_espec)
