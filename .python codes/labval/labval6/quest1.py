nome= input("digite o nome da pessoa: ")

with open ( "dados.txt", "a", encoding = "utf-8") as arquivo:
    arquivo.write (nome + "\n")
print("Dado inserido com sucesso no arquivo 'dados .txt' ")