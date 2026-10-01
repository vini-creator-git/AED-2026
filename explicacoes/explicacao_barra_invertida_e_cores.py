"""Guia sobre a barra invertida, escapes e cores no terminal."""

# A barra invertida inicia uma sequencia de escape dentro de uma string.
# Ela permite representar caracteres especiais sem digita-los diretamente.
print("Linha 1\nLinha 2")
print("Coluna 1\tColuna 2")

# Escapes mais usados:
# \n  nova linha
# \t  tabulacao
# \r  volta o cursor para o inicio da linha
# \b  retrocesso
# \f  quebra de pagina
# \v  tabulacao vertical
# \a  alerta sonoro, dependendo do terminal
# \\  uma barra invertida literal
# \'  aspas simples dentro de string com aspas simples
# \"  aspas duplas dentro de string com aspas duplas
print("Barra invertida: \\")
print('Asposta simples: \'')
print("Aspas duplas: \"")

# A sequencia octal usa de 1 a 3 digitos apos a barra.
print("Codigo octal para A: \101")

# A sequencia hexadecimal usa exatamente dois digitos apos \x.
print("Codigo hexadecimal para A: \x41")

# \u representa um caractere Unicode com quatro digitos hexadecimais.
# \U representa um caractere Unicode com oito digitos hexadecimais.
print("Coracao Unicode: \u2665")
print("Simbolo Unicode: \U0001F680")

# A funcao ord() transforma um caractere em seu numero Unicode.
# chr() faz o caminho inverso.
print("Codigo de A:", ord("A"))
print("Caractere 65:", chr(65))

# Strings raw ignoram a interpretacao da maioria dos escapes.
# Sao uteis para caminhos e expressoes regulares.
caminho_raw = r"C:\Users\Ana\Documentos\arquivo.txt"
print("Caminho raw:", caminho_raw)

# Uma string comum precisaria duplicar cada barra em um caminho Windows.
caminho_comum = "C:\\Users\\Ana\\Documentos\\arquivo.txt"
print("Caminho comum:", caminho_comum)

# Raw strings nao podem terminar com uma unica barra invertida.
# r"C:\" e invalida. Use r"C:\\" ou "C:\\\\".

# Em expressoes regulares, a barra invertida tambem cria classes e escapes.
import re

padrao = r"\d+"
print("Numeros encontrados:", re.findall(padrao, "Sala 12, bloco 3"))

# Uma barra invertida no final da linha continua a expressao na linha seguinte.
# Esse recurso existe, mas parenteses sao mais legiveis para expressao longa.
total = 1 + 2 + 3 + \
        4 + 5
print("Total com continuacao de linha:", total)

total_com_parenteses = (
    1 + 2 + 3
    + 4 + 5
)
print("Total com parenteses:", total_com_parenteses)

# Cuidado: uma barra invertida antes de uma letra desconhecida pode gerar
# um aviso ou mudar o significado no futuro. Use raw strings quando fizer sentido.

# -----------------------------------------------------------------------------
# CORES ANSI
# -----------------------------------------------------------------------------
# Terminais entendem sequencias ANSI. Elas normalmente comecam com ESC,
# representado em Python por \033, \x1b ou \u001b.
ESC = "\033["
RESET = ESC + "0m"

PRETO = ESC + "30m"
VERMELHO = ESC + "31m"
VERDE = ESC + "32m"
AMARELO = ESC + "33m"
AZUL = ESC + "34m"
MAGENTA = ESC + "35m"
CIANO = ESC + "36m"
BRANCO = ESC + "37m"

print(VERMELHO + "Texto vermelho" + RESET)
print(VERDE + "Texto verde" + RESET)
print(AZUL + "Texto azul" + RESET)
print(CIANO + "Texto ciano" + RESET)

# Resetar sempre evita que a cor continue nos proximos textos.

# Cores claras usam 90 a 97.
CINZA = ESC + "90m"
VERMELHO_CLARO = ESC + "91m"
VERDE_CLARO = ESC + "92m"
print(CINZA + "Cinza" + RESET)
print(VERDE_CLARO + "Verde claro" + RESET)

# Cores de fundo usam 40 a 47; fundos claros usam 100 a 107.
FUNDO_VERMELHO = ESC + "41m"
FUNDO_AZUL = ESC + "44m"
FUNDO_CINZA = ESC + "100m"
print(FUNDO_VERMELHO + " Fundo vermelho " + RESET)
print(FUNDO_AZUL + " Fundo azul " + RESET)
print(FUNDO_CINZA + " Fundo cinza claro " + RESET)

# Estilos: 1 negrito, 2 fraco, 3 italico, 4 sublinhado,
# 7 invertido, 9 tachado e 22/23/24/27/29 para desfazer alguns estilos.
NEGRITO = ESC + "1m"
ITALICO = ESC + "3m"
SUBLINHADO = ESC + "4m"
TACHADO = ESC + "9m"
print(NEGRITO + "Negrito" + RESET)
print(ITALICO + "Italico" + RESET)
print(SUBLINHADO + "Sublinhado" + RESET)
print(TACHADO + "Tachado" + RESET)

# E possivel combinar codigos com ponto e virgula.
NEGRITO_AMARELO = ESC + "1;33m"
print(NEGRITO_AMARELO + "Negrito amarelo" + RESET)

# -----------------------------------------------------------------------------
# 256 CORES E RGB
# -----------------------------------------------------------------------------
# 256 cores: texto 38;5;N e fundo 48;5;N, com N entre 0 e 255.
def texto_256(codigo, texto):
    return f"{ESC}38;5;{codigo}m{texto}{RESET}"


def fundo_256(codigo, texto):
    return f"{ESC}48;5;{codigo}m{texto}{RESET}"


print(texto_256(208, "Laranja em 256 cores"))
print(fundo_256(25, "Fundo azul em 256 cores"))

# True color usa tres valores entre 0 e 255 para vermelho, verde e azul.
def texto_rgb(vermelho, verde, azul, texto):
    return f"{ESC}38;2;{vermelho};{verde};{azul}m{texto}{RESET}"


print(texto_rgb(255, 120, 0, "Laranja RGB"))

# Exemplo pratico com uma funcao para imprimir mensagens coloridas.
def mensagem_status(mensagem, sucesso=True):
    cor = VERDE if sucesso else VERMELHO
    simbolo = "OK" if sucesso else "ERRO"
    print(f"{cor}[{simbolo}] {mensagem}{RESET}")


mensagem_status("Arquivo processado")
mensagem_status("Arquivo nao encontrado", sucesso=False)

# Nem todo terminal suporta todos os estilos e cores.
# Em terminais modernos do Windows, Linux e macOS, ANSI costuma funcionar.
# Se os codigos aparecerem escritos na tela, o terminal nao os interpretou.

# Resumo:
# 1. Use \\ para escrever uma barra invertida literal.
# 2. Use \u ou \U para caracteres Unicode.
# 3. Use strings raw para caminhos e regex com muitas barras.
# 4. Use \033[...m para controlar cores e estilos ANSI.
# 5. Use RESET depois de uma cor ou estilo.
