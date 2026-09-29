peso = float(input())
litros_bebidos = float(input())

# 35ml por kg equivale a (peso * 35) / 1000 litros
meta_litros = (peso * 35) / 1000
print(litros_bebidos >= meta_litros)