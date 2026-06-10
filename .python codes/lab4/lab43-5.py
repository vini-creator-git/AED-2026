valor = int(input("Digite o valor da compra?"))
dist = int(input("Qual a distância?"))
final = valor >= 200 and dist <= 100
final2 = valor < 200 and dist>100
print(f"Seu frete final é de {final, final2 + 20}")