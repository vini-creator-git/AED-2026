maiores_de_idade = []
with open("dados.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
        nome, idade_str = linha_limpa.split(",")
        idade = int(idade_str)
        if idade >= 18:
            maiores_de_idade.append({"nome": nome, "idade": idade})

print("Pessoas Maiores de idade extraídas")
for pessoa in maiores_de_idade:
    print(f"- {pessoa['nome']} ({pessoa['idade']} anos)")