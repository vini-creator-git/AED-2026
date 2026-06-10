#Guerreiro = força >= 15, magia <= 10
#Mago = força <= 10, magia >= 15
#Arqueiro = magia > 5  and <= 15 -> magia e força ==
classe = input("Escolha a classe (guerreiro, mago ou arqueiro): ")
magia  = int(input())
força = int(input())
guerreiro = classe == "guerreiro" and magia <= 10 and força >= 15
mago = classe == "mago" and magia >= 15 and força <= 10
arqueiro = classe == "arqueiro" and 15 >= magia >= 5 and 15 >= força >= 5
print(f"Personagem válido{guerreiro or mago or arqueiro}")
