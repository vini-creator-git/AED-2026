import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
janela.title("Aplicativo exemplo")
janela.geometry("400x250")

label = tk.Label(janela, text="Digite seu nome:")
label.pack(pady=10)

entrada = tk.Entry(janela, width=30)
entrada.pack()

nome = tk.StringVar()


def mostrar():
    nome.set(entrada.get())
    mensagem = tk.Label(janela, text=f"Olá, {nome.get()}!")
    mensagem.pack(pady=10)

botao = ttk.Button(janela, text="Enviar", command=mostrar)
botao.pack()

janela.mainloop()