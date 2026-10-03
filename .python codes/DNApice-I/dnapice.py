from random import choice

bases = {"A": "T", "T": "A", "C": "G", "G": "C"}
rnab = {"A": "U", "T": "A", "C": "G", "G": "C"}
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
