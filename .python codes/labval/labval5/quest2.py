#2) lendo o arquivo (r) ---> lendo o arquivo todo de uma vez
with open ("exemplo.txt", "r", encoding = "UTF-8") as arquivo:
    conteudo=arquivo.read()
    print("----conteudo do arquivo-----")
    print(conteudo)

