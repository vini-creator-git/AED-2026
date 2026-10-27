#3) lendo o arquivo linha por linha
with open ("exemplo.txt", "r", encoding = "UTF-8") as arquivo:
    for linha in arquivo:
        print(f"linha:{linha.strip()}")