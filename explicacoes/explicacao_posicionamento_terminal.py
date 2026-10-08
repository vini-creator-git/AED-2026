"""Guia para posicionar texto e elementos no terminal com Python.

O terminal trabalha como uma grade de caracteres: cada linha tem colunas.
Por isso, "mudar a posicao" normalmente significa controlar:

1. a quantidade de espacos antes do texto;
2. o alinhamento dentro de uma largura fixa;
3. a linha e a coluna onde o cursor deve ser colocado.
"""

import os
import shutil


# ---------------------------------------------------------------------------
# ALINHAMENTO HORIZONTAL
# ---------------------------------------------------------------------------
# center(), ljust() e rjust() recebem a largura total ocupada pelo texto.
titulo = "MENU PRINCIPAL"

print(titulo.center(40))  # centralizado em uma area de 40 colunas
print(titulo.ljust(40))  # encostado a esquerda
print(titulo.rjust(40))  # encostado a direita

# O segundo argumento define o caractere usado para preencher o espaco.
print(titulo.center(40, "="))
print(titulo.ljust(40, "."))
print(titulo.rjust(40, "-"))


# ---------------------------------------------------------------------------
# CENTRALIZAR UMA MOLDURA
# ---------------------------------------------------------------------------
def imprimir_moldura(texto, largura=40):
    """Imprime uma caixa centralizada na largura informada."""
    linhas = [
        "+" + "-" * (largura - 2) + "+",
        "|" + texto.center(largura - 2) + "|",
        "+" + "-" * (largura - 2) + "+",
    ]

    for linha in linhas:
        print(linha.center(largura))


imprimir_moldura("DNApice", largura=50)


# ---------------------------------------------------------------------------
# USANDO F-STRINGS PARA ALINHAR COLUNAS
# ---------------------------------------------------------------------------
# O numero depois de : indica a largura do campo.
print(f"{'Nome':<15}{'Nota':>6}{'Situacao':^12}")
print(f"{'Ana':<15}{9.5:>6.1f}{'Aprovada':^12}")
print(f"{'Bia':<15}{7.0:>6.1f}{'Aprovada':^12}")

# < alinha a esquerda, > alinha a direita e ^ centraliza.
# O preenchimento pode ser colocado antes do alinhamento:
print(f"{'Titulo':=^30}")


# ---------------------------------------------------------------------------
# CENTRALIZAR DE ACORDO COM O TAMANHO REAL DO TERMINAL
# ---------------------------------------------------------------------------
def imprimir_centralizado(texto):
    """Centraliza texto usando a quantidade atual de colunas do terminal."""
    largura_terminal = shutil.get_terminal_size(fallback=(80, 24)).columns
    print(texto.center(largura_terminal))


imprimir_centralizado("Esta frase acompanha a largura do terminal")


# ---------------------------------------------------------------------------
# POSICIONAR O CURSOR COM SEQUENCIAS ANSI
# ---------------------------------------------------------------------------
# \033[LINHA;COLUNAm move o cursor para uma posicao especifica.
# A contagem de linhas e colunas comeca em 1.
ESC = "\033["


def posicionar_cursor(linha, coluna):
    """Move o cursor para a linha e a coluna informadas."""
    print(f"{ESC}{linha};{coluna}H", end="")


# Limpa a tela e coloca o cursor no canto superior esquerdo.
print(f"{ESC}2J{ESC}H", end="")
posicionar_cursor(3, 10)
print("Texto na linha 3, coluna 10")

# Depois de usar ANSI, e uma boa pratica devolver o cursor para o final.
posicionar_cursor(5, 1)
print("Texto depois do exemplo")


# ---------------------------------------------------------------------------
# POSICIONAMENTO VERTICAL
# ---------------------------------------------------------------------------
def imprimir_no_centro_da_tela(texto):
    """Tenta centralizar uma linha vertical e horizontalmente."""
    tamanho = shutil.get_terminal_size(fallback=(80, 24))
    linhas_acima = max((tamanho.lines - 1) // 2, 0)

    # \n cria linhas vazias antes do texto.
    print("\n" * linhas_acima, end="")
    print(texto.center(tamanho.columns))


# Descomente para testar:
# os.system("cls" if os.name == "nt" else "clear")
# imprimir_no_centro_da_tela("Bem-vindo!")


# ---------------------------------------------------------------------------
# RESUMO
# ---------------------------------------------------------------------------
# texto.center(largura) -> centraliza horizontalmente.
# texto.ljust(largura)  -> alinha a esquerda.
# texto.rjust(largura)  -> alinha a direita.
# f"{texto:^20}"         -> centraliza em um campo de 20 colunas.
# f"{texto:<20}"         -> alinha a esquerda em um campo de 20 colunas.
# f"{texto:>20}"         -> alinha a direita em um campo de 20 colunas.
# shutil.get_terminal_size() -> descobre o tamanho atual do terminal.
# \033[linha;colunaH      -> move o cursor para uma linha e coluna.
# \033[2J                -> limpa a tela.
# \033[H                 -> move o cursor para o inicio.
#
# Observacao: sequencias ANSI funcionam na maioria dos terminais modernos.
# Se os simbolos aparecerem escritos na tela, o terminal pode nao ter suporte.
# Tambem e importante lembrar que caracteres Unicode podem ocupar uma largura
# visual diferente de 1 coluna; para interfaces muito precisas, use ASCII.
