with open("pessoas.csv", "a", encoding="utf-8")as arquivo:
    print("***cadastro de pessoas***")
    while True:
        nome=input("\nNome: ")
        idade=input("\nIdade: ")
        cidade=input("\nCidade: ")
        linha=(f"{nome}, {idade} anos, {cidade} \n")
        arquivo.write(linha)
        continuar=input("\n deseja cadastrar outra pessoa?(s/n) ")
        if continuar.lower() != "s":
            break
print("\n cadastro concluido! dados salvos em 'pessoas.csv' ")
