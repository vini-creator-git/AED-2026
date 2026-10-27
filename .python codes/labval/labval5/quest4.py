#4)ADICIONANDO CONTEUDO SEM SOBRESCREVER
with open ("exemplo.txt", "a", encoding = "UTF-8") as arquivo:
    arquivo.write("terceira linha adicionada depois!\n")
    print("nova linha anexada!")