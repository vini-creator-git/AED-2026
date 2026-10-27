#1) criando e escrevendo um arquivo (w)
with open ("exemplo.txt", "w", encoding = "UTF-8") as arquivo:
    arquivo.write("primeira linha do arquivo.\n")
    arquivo.write("segunda linha com python.\n")
print("arquivo criado com sucesso")



