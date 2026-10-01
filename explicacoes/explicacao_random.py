"""Guia pratico dos principais recursos do modulo random."""

import random

# random gera valores pseudoaleatorios. Eles parecem aleatorios,
# mas sao produzidos por um algoritmo deterministico.

# seed() fixa o ponto inicial. Isso torna o exemplo reproduzivel.
random.seed(42)

# random() retorna um float no intervalo [0.0, 1.0).
print("Float entre 0 e 1:", random.random())

# uniform(a, b) retorna um float entre a e b.
print("Float entre 10 e 20:", random.uniform(10, 20))

# randint(a, b) inclui os dois limites.
print("Inteiro entre 1 e 6:", random.randint(1, 6))

# randrange() funciona como range(): o limite final fica de fora.
print("Inteiro par entre 0 e 10:", random.randrange(0, 11, 2))

# choice() escolhe um elemento.
frutas = ["maca", "banana", "uva", "laranja"]
print("Uma fruta:", random.choice(frutas))

# choices() permite repeticao e pode sortear varios elementos.
print("Tres frutas, com repeticao:", random.choices(frutas, k=3))

# weights permite dar pesos diferentes para cada opcao.
cores = ["azul", "verde", "vermelho"]
print("Cor ponderada:", random.choices(cores, weights=[1, 2, 1], k=1))

# sample() escolhe elementos sem repeticao.
print("Duas frutas, sem repeticao:", random.sample(frutas, k=2))

# shuffle() embaralha a propria lista e retorna None.
baralho = list(range(1, 11))
random.shuffle(baralho)
print("Lista embaralhada:", baralho)

# Para nao alterar a lista original, use uma copia.
frutas_embaralhadas = frutas.copy()
random.shuffle(frutas_embaralhadas)
print("Original:", frutas)
print("Copia embaralhada:", frutas_embaralhadas)

# getrandbits(k) retorna um inteiro formado por k bits aleatorios.
print("Oito bits:", random.getrandbits(8))

# distribuicoes estatisticas para simulacoes:
print("Normal:", random.normalvariate(10, 2))
print("Triangular:", random.triangular(0, 10, 4))
print("Exponencial:", random.expovariate(1.5))

# Uma semente diferente geralmente produz outra sequencia.
random.seed(7)
print("Sequencia reproduzivel:", [random.randint(1, 100) for _ in range(5)])
random.seed(7)
print("Mesma sequencia novamente:", [random.randint(1, 100) for _ in range(5)])

# Exemplo: gerar uma base de DNA aleatoria.
random.seed(10)
bases = "ATCG"
sequencia = "".join(random.choices(bases, k=10))
print("Sequencia de DNA:", sequencia)

# O modulo random NAO deve ser usado para senhas, tokens ou criptografia.
# Para isso, use secrets:
# import secrets
# token = secrets.token_urlsafe(16)

# Funcoes mais usadas:
# random, uniform, randint, randrange, choice, choices, sample,
# shuffle, seed e getrandbits.
