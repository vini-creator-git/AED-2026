km_por_litro = float(input("Quantos km seu carro percorre por litro? "))
km_viagem = float(input("Quantos km você pretende viajar? "))
valor_combustivel = float(input("Qual o valor do combustível? "))
pedagio = float(input("Quanto vai gastar de pedágio? "))
pessoas = int(input("Quantas pessoas vão dividir a conta? "))

custo_combustivel = (km_viagem / km_por_litro) * valor_combustivel
custo_total = (custo_combustivel + pedagio) / pessoas

print(f"Cada pessoa gastará R${custo_total:.2f}")
