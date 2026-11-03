with open ("lista.txt", "a", encoding= "utf-8" )as arquivo2:
    print ("-----cadastro de nomes(digite 'sair' para encerrar)------")
    while True:
        dado=input("digite uma informacao: ")
        if dado.lower()== "sair":
            break
        arquivo2.write (dado + "\n")
        print("***registrado***")
print("processo finalizado. todos os dados foram salvoa em 'lista.txt'! ")
