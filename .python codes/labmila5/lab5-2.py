idade = int(input("Qual é a sua idade? "))

if idade >= 18:
    license = input("Você possui carteira de motorista? (s/n): ");
    
    if license == "s":
        print("Você pode dirigir!")
    else:
        print("Você não pode dirigir sem carteira de motorista.")
else:
    print("Você não tem idade suficiente para dirigir.")