# Tkinter: conceitos, exemplos e uma janela final com todos os exemplos

Tkinter é a biblioteca padrão de interface gráfica do Python. Ela permite criar janelas, botões, campos de texto, listas, menus e outros elementos visuais com pouco código.

Ele é muito usado em projetos didáticos, protótipos, aplicações simples e ferramentas internas. A grande vantagem é que ele já vem junto com o Python, então você não precisa instalar nada extra para começar.

---

## 1. O que é Tkinter?

Tkinter é um conjunto de ferramentas em Python que permite criar interfaces gráficas. Internamente ele usa o toolkit Tk, que é uma biblioteca de interface gráfica multiplataforma.

Em outras palavras:
- `Tkinter` = conjunto de classes e funções em Python
- `Tk` = engine visual que desenha os elementos na tela

A ideia é simples: você cria objetos que representam componentes visuais, configura suas propriedades e organiza eles na janela.

### Exemplo mínimo

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Primeira janela")
janela.geometry("300x200")

label = tk.Label(janela, text="Olá, mundo!")
label.pack()

janela.mainloop()
```

### O que esse código faz?

- `tk.Tk()` cria a janela principal
- `title()` define o título da janela
- `geometry()` define o tamanho inicial da janela
- `tk.Label(...)` cria um texto na tela
- `pack()` organiza o label na janela
- `mainloop()` mantém a janela aberta e responsiva

---

## 2. Estrutura básica de um programa em Tkinter

Um programa em Tkinter normalmente segue esta ordem:

1. importar o módulo
2. criar a janela principal
3. criar widgets
4. configurar os widgets
5. posicionar os widgets
6. chamar `mainloop()`

### Estrutura padrão

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Meu programa")
janela.geometry("400x300")

# widgets
label = tk.Label(janela, text="Texto")
label.pack()

# loop principal
janela.mainloop()
```

### Conceito importante: widget

Um widget é qualquer elemento visual da interface, como:
- label
- botão
- entrada de texto
- caixa de seleção
- lista
- menu
- janela

---

## 3. A janela principal: Tk()

A janela principal é criada com `Tk()`.

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Janela principal")
janela.geometry("500x300")

janela.mainloop()
```

### Propriedades comuns da janela

```python
janela.title("Meu aplicativo")
janela.geometry("500x300")
janela.resizable(False, False)
janela.configure(bg="white")
```

### O que significa cada um?

- `title()`: título da janela
- `geometry()`: tamanho inicial em pixels
- `resizable()`: permite ou bloqueia redimensionamento
- `configure()`: altera propriedades visuais da janela

---

## 4. Label: exibindo texto

`Label` serve para mostrar texto ou imagem.

### Exemplo simples

```python
import tkinter as tk

janela = tk.Tk()
janela.geometry("250x100")

texto = tk.Label(janela, text="Bem-vindo ao Tkinter!")
texto.pack()

janela.mainloop()
```

### Personalizando o label

```python
label = tk.Label(
    janela,
    text="Texto bonito",
    font=("Arial", 16, "bold"),
    fg="blue",
    bg="lightgray",
    padx=20,
    pady=10
)
label.pack()
```

### Parâmetros úteis

- `text`: texto exibido
- `font`: fonte
- `fg`: cor da letra
- `bg`: cor de fundo
- `padx`, `pady`: espaçamento interno

---

## 5. Button: botões clicáveis

`Button` cria um botão que pode executar uma ação ao ser clicado.

### Exemplo básico

```python
import tkinter as tk

janela = tk.Tk()

def clique():
    print("Botão clicado!")

botao = tk.Button(janela, text="Clique aqui", command=clique)
botao.pack(pady=20)

janela.mainloop()
```

### Explicando o código

- `command=clique` diz ao Tkinter que função deve ser chamada ao clicar
- ao clicar, a função `clique()` executa

### Botão com estilo

```python
botao = tk.Button(
    janela,
    text="Enviar",
    width=15,
    height=2,
    bg="green",
    fg="white",
    font=("Arial", 12, "bold")
)
botao.pack()
```

---

## 6. Entry: entrada de texto

`Entry` é usado para receber texto do usuário.

### Exemplo

```python
import tkinter as tk

janela = tk.Tk()
janela.title("Entrada")

label = tk.Label(janela, text="Digite seu nome:")
label.pack()

entrada = tk.Entry(janela, width=30)
entrada.pack(pady=10)

janela.mainloop()
```

### Pegando o valor digitado

```python
import tkinter as tk

janela = tk.Tk()

entrada = tk.Entry(janela, width=30)
entrada.pack(pady=10)

label_resultado = tk.Label(janela, text="")
label_resultado.pack()


def mostrar():
    nome = entrada.get()
    label_resultado.config(text=f"Olá, {nome}!")


botao = tk.Button(janela, text="Mostrar", command=mostrar)
botao.pack()

janela.mainloop()
```

### Métodos importantes

- `get()`: pega o texto digitado
- `delete()`: apaga o conteúdo
- `insert()`: insere texto dentro do campo

---

## 7. Text: área de texto multilinha

`Text` permite escrever várias linhas, como um editor simples.

```python
import tkinter as tk

janela = tk.Tk()

texto = tk.Text(janela, width=40, height=10)
texto.pack(pady=10)

janela.mainloop()
```

### Lendo o conteúdo do Text

```python
conteudo = texto.get("1.0", "end")
print(conteudo)
```

Explicando:
- `"1.0"` = linha 1, coluna 0
- `"end"` = final do texto

---

## 8. Frame: agrupando widgets

`Frame` funciona como um container. Ele organiza widgets em grupos e ajuda no layout.

```python
import tkinter as tk

janela = tk.Tk()

frame = tk.Frame(janela, bg="lightblue", padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Dentro do Frame")
label.pack()

botao = tk.Button(frame, text="Botão")
botao.pack(pady=5)

janela.mainloop()
```

### Quando usar Frame?

- para separar grupos de elementos
- para deixar a interface organizada
- para criar blocos visuais

---

## 9. Checkbutton: caixa de seleção

`Checkbutton` serve para opções do tipo sim/não.

```python
import tkinter as tk

janela = tk.Tk()

valor = tk.BooleanVar()
valor.set(False)

check = tk.Checkbutton(janela, text="Aceito os termos", variable=valor)
check.pack()

janela.mainloop()
```

### Pegando o valor

```python
if valor.get():
    print("Marcado")
else:
    print("Não marcado")
```

---

## 10. Radiobutton: opções exclusivas

`Radiobutton` é usado quando o usuário deve escolher uma única opção.

```python
import tkinter as tk

janela = tk.Tk()

opcao = tk.StringVar()
opcao.set("Python")

rb1 = tk.Radiobutton(janela, text="Python", variable=opcao, value="Python")
rb2 = tk.Radiobutton(janela, text="Java", variable=opcao, value="Java")
rb3 = tk.Radiobutton(janela, text="C++", variable=opcao, value="C++")

rb1.pack()
rb2.pack()
rb3.pack()

janela.mainloop()
```

### Observação importante

Todos os `Radiobutton`s devem compartilhar a mesma variável (`variable`) para que a escolha seja exclusiva.

---

## 11. Listbox: lista de opções

`Listbox` mostra uma lista de itens e permite selecionar um ou mais deles.

```python
import tkinter as tk

janela = tk.Tk()

lista = tk.Listbox(janela)
lista.insert(1, "Python")
lista.insert(2, "Java")
lista.insert(3, "C++")
lista.pack()

janela.mainloop()
```

### Pegar item selecionado

```python
indice = lista.curselection()
if indice:
    item = lista.get(indice[0])
    print(item)
```

---

## 12. Scale: controle deslizante

`Scale` cria um controle deslizante para escolher valores numéricos.

```python
import tkinter as tk

janela = tk.Tk()

slider = tk.Scale(janela, from_=0, to=100, orient=tk.HORIZONTAL)
slider.pack()

janela.mainloop()
```

### Obter valor

```python
valor = slider.get()
print(valor)
```

---

## 13. Canvas: desenhando na tela

`Canvas` permite desenhar formas, linhas, retângulos, círculos e outros objetos gráficos.

```python
import tkinter as tk

janela = tk.Tk()
canvas = tk.Canvas(janela, width=300, height=200, bg="white")
canvas.pack()

canvas.create_line(10, 10, 200, 150, fill="blue", width=3)
canvas.create_rectangle(50, 50, 150, 120, fill="red")
canvas.create_oval(180, 40, 260, 110, fill="green")

janela.mainloop()
```

### Quando usar Canvas?

- gráficos
- desenhos simples
- jogos simples
- diagramas

---

## 14. Organização visual: pack(), grid() e place()

Tkinter tem 3 formas principais de organizar widgets.

### 14.1 pack()
Empilha os widgets em sequência.

```python
label1 = tk.Label(janela, text="Primeiro")
label2 = tk.Label(janela, text="Segundo")

label1.pack()
label2.pack()
```

### 14.2 grid()
Organiza em linhas e colunas.

```python
label = tk.Label(janela, text="Nome:")
label.grid(row=0, column=0)

entrada = tk.Entry(janela)
entrada.grid(row=0, column=1)
```

### 14.3 place()
Posiciona em coordenadas específicas.

```python
botao = tk.Button(janela, text="Botão")
botao.place(x=80, y=50)
```

### Qual usar?

- `pack()`: fácil para layouts simples
- `grid()`: melhor para formulários e telas mais organizadas
- `place()`: ideal para ajuste preciso de posições

---

## 15. Propriedades dos widgets

Muitos widgets aceitam parâmetros como:

- `text`
- `font`
- `fg`
- `bg`
- `width`
- `height`
- `padx`
- `pady`
- `command`

### Exemplo completo

```python
botao = tk.Button(
    janela,
    text="Enviar",
    width=15,
    height=2,
    bg="blue",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5,
    command=lambda: print("Executou!")
)
```

### O que cada um faz?

- `width` e `height`: tamanho
- `bg`: cor de fundo
- `fg`: cor do texto
- `font`: estilo da fonte
- `padx` e `pady`: distância interna

---

## 16. Eventos e callbacks

Eventos são ações feitas pelo usuário, como:
- clique em botão
- pressionar tecla
- passar o mouse sobre um objeto
- fechar a janela

A função responsável por responder ao evento é chamada de callback.

### Exemplo com botão

```python
import tkinter as tk

janela = tk.Tk()


def clicar():
    print("Você clicou no botão!")


botao = tk.Button(janela, text="Clique", command=clicar)
botao.pack()

janela.mainloop()
```

### Evento de teclado

```python
import tkinter as tk

janela = tk.Tk()


def pressionou(event):
    print("Tecla pressionada:", event.keysym)


janela.bind("<KeyPress>", pressionou)
janela.mainloop()
```

### Por que isso é importante?

Porque a interface gráfica fica interativa. O programa reage ao que o usuário faz.

---

## 17. Variáveis do Tkinter

Tkinter possui tipos especiais de variáveis para guardar valores que serão exibidos ou alterados em widgets.

### 17.1 StringVar

Usada para texto.

```python
import tkinter as tk

janela = tk.Tk()

nome = tk.StringVar()
nome.set("Ana")

label = tk.Label(janela, textvariable=nome)
label.pack()

janela.mainloop()
```

### 17.2 IntVar

Usada para números inteiros.

```python
valor = tk.IntVar()
valor.set(10)
print(valor.get())
```

### 17.3 DoubleVar

Usada para números decimais.

```python
numero = tk.DoubleVar()
numero.set(3.14)
```

### 17.4 BooleanVar

Usada para verdadeiro/falso.

```python
ativo = tk.BooleanVar()
ativo.set(True)
```

### Por que usar essas variáveis?

Porque elas se conectam melhor aos widgets e ficam sincronizadas com a interface.

---

## 18. Menus

Tkinter também permite criar menus na janela.

```python
import tkinter as tk

janela = tk.Tk()

menu_principal = tk.Menu(janela)
janela.config(menu=menu_principal)

arquivo = tk.Menu(menu_principal, tearoff=0)
arquivo.add_command(label="Abrir")
arquivo.add_command(label="Salvar")
arquivo.add_separator()
arquivo.add_command(label="Sair")

menu_principal.add_cascade(label="Arquivo", menu=arquivo)

janela.mainloop()
```

### O que é `tearoff`?

É um parâmetro que remove a linha de separação padrão do menu.

---

## 19. Mensagens e caixas de diálogo

Tkinter oferece funções para mostrar mensagens.

### messagebox

```python
from tkinter import messagebox

messagebox.showinfo("Informação", "Operação concluída!")
messagebox.showwarning("Atenção", "Cuidado!")
messagebox.showerror("Erro", "Algo deu errado")
```

### filedialog

Permite abrir ou salvar arquivos.

```python
from tkinter import filedialog

arquivo = filedialog.askopenfilename()
print(arquivo)
```

Essas janelas são muito úteis em aplicações reais.

---

## 20. ttk: widgets mais modernos

O módulo `ttk` fornece widgets com visual mais bonito e mais moderno, geralmente melhorando a aparência da interface.

```python
import tkinter as tk
from tkinter import ttk

janela = tk.Tk()

botao = ttk.Button(janela, text="Botão ttk")
botao.pack(pady=20)

janela.mainloop()
```

### Widgets comuns do ttk

- `Button`
- `Label`
- `Entry`
- `Combobox`
- `Checkbutton`
- `Radiobutton`
- `Treeview`

---

## 21. Combobox: caixa de seleção com opções

```python
import tkinter as tk
from tkinter import ttk

janela = tk.Tk()

opcoes = ["Python", "Java", "C++", "JavaScript"]
combo = ttk.Combobox(janela, values=opcoes)
combo.set("Python")
combo.pack(pady=20)

janela.mainloop()
```

### Como pegar a opção selecionada?

```python
valor = combo.get()
print(valor)
```

---

## 22. Treeview: tabela em árvore

`Treeview` é usado para exibir dados em formato de tabela ou árvore.

```python
import tkinter as tk
from tkinter import ttk

janela = tk.Tk()

arvore = ttk.Treeview(janela, columns=("nome", "idade"), show="headings")
arvore.heading("nome", text="Nome")
arvore.heading("idade", text="Idade")
arvore.insert("", "end", values=("Ana", 20))
arvore.insert("", "end", values=("Pedro", 25))
arvore.pack()

janela.mainloop()
```

### O que é `show="headings"`?

Ele faz com que o cabeçalho das colunas apareça na tabela.

---

## 23. Configuração de janela e aparência

Você pode configurar vários aspectos visuais e de comportamento da janela.

```python
janela.title("Meu app")
janela.geometry("600x400")
janela.resizable(False, False)
janela.configure(bg="white")
```

### Parâmetros importantes

- `title()`: título da janela
- `geometry()`: tamanho inicial
- `resizable()`: permite ou bloqueia ajuste
- `configure()`: altera propriedades da interface

---

## 24. mainloop(): o coração da interface

`mainloop()` é o comando que mantém a interface aberta e executando.

```python
janela.mainloop()
```

Sem esse comando, a janela pode abrir e fechar instantaneamente. Ele é responsável por:
- manter a aplicação em execução
- processar eventos do mouse e teclado
- atualizar os widgets

---

## 25. Exemplo completo com vários elementos

Abaixo está um exemplo que reúne vários conceitos importantes do Tkinter em uma mesma janela:

```python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

janela = tk.Tk()
janela.title("Exemplo completo em Tkinter")
janela.geometry("500x500")

# Label
label = tk.Label(janela, text="Digite seu nome:", font=("Arial", 12))
label.pack(pady=(20, 5))

# Entry
entrada = tk.Entry(janela, width=30)
entrada.pack()

# StringVar
nome = tk.StringVar()

# Checkbutton
aceito = tk.BooleanVar()
check = tk.Checkbutton(janela, text="Aceito os termos", variable=aceito)
check.pack(pady=10)

# Combobox
opcoes = ["Python", "Java", "C++", "JavaScript"]
combo = ttk.Combobox(janela, values=opcoes)
combo.set("Python")
combo.pack(pady=10)

# Botão

def mostrar():
    texto = entrada.get()
    if not texto:
        messagebox.showwarning("Campo vazio", "Digite um nome!")
        return
    nome.set(texto)
    mensagem = f"Olá, {nome.get()}! Você escolheu {combo.get()}."
    if aceito.get():
        mensagem += " Você aceitou os termos."
    else:
        mensagem += " Você ainda não aceitou os termos."
    result_label.config(text=mensagem)


botao = tk.Button(janela, text="Enviar", command=mostrar, bg="blue", fg="white")
botao.pack(pady=10)

result_label = tk.Label(janela, text="", font=("Arial", 10), wraplength=350)
result_label.pack(pady=10)

janela.mainloop()
```

---

## 26. Boas práticas em Tkinter

- prefira `grid()` para layouts mais organizados
- use `ttk` quando quiser uma aparência mais moderna
- mantenha funções de evento simples e bem nomeadas
- evite misturar `pack()` e `grid()` na mesma janela
- use `StringVar`, `IntVar` e `BooleanVar` para conectar dados à interface
- se necessário, separe a lógica da interface em funções

---

## 27. Resumo final

Tkinter é uma biblioteca essencial para criar interfaces gráficas em Python. Os conceitos principais são:

- `Tk()` para criar a janela principal
- widgets para criar elementos visuais
- `pack()`, `grid()` e `place()` para organizar a interface
- eventos e callbacks para responder às ações do usuário
- variáveis como `StringVar` e `BooleanVar`
- `ttk` para widgets mais modernos
- `mainloop()` para manter a janela aberta

Com esses fundamentos, você já consegue criar programas interativos e bastante úteis.

---

## 28. Janela final com todos os exemplos

Abaixo está um único código que reúne vários exemplos em uma única janela. Ele funciona como uma pequena "galeria" de conceitos do Tkinter.

```python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

janela = tk.Tk()
janela.title("Tkinter - Galeria de exemplos")
janela.geometry("800x700")

# ---------- Exemplo 1: Label ----------
label = tk.Label(janela, text="Exemplo 1: Label", font=("Arial", 12, "bold"))
label.pack(pady=(15, 5))
texto = tk.Label(janela, text="Olá, mundo!", fg="blue")
texto.pack()

# ---------- Exemplo 2: Entry + Button ----------
entrada_label = tk.Label(janela, text="Exemplo 2: Entry", font=("Arial", 12, "bold"))
entrada_label.pack(pady=(20, 5))
entrada = tk.Entry(janela, width=30)
entrada.pack()
resultado = tk.Label(janela, text="")
resultado.pack(pady=5)


def mostrar_entrada():
    valor = entrada.get()
    if valor:
        resultado.config(text=f"Você digitou: {valor}")
    else:
        resultado.config(text="Campo vazio!")

botao_entrada = tk.Button(janela, text="Mostrar valor", command=mostrar_entrada)
botao_entrada.pack()

# ---------- Exemplo 3: Checkbutton ----------
check_label = tk.Label(janela, text="Exemplo 3: Checkbutton", font=("Arial", 12, "bold"))
check_label.pack(pady=(20, 5))
aceito = tk.BooleanVar()
check = tk.Checkbutton(janela, text="Aceito os termos", variable=aceito)
check.pack()

# ---------- Exemplo 4: Radiobutton ----------
radio_label = tk.Label(janela, text="Exemplo 4: Radiobutton", font=("Arial", 12, "bold"))
radio_label.pack(pady=(20, 5))
linguagem = tk.StringVar(value="Python")
rb1 = tk.Radiobutton(janela, text="Python", variable=linguagem, value="Python")
rb2 = tk.Radiobutton(janela, text="Java", variable=linguagem, value="Java")
rb3 = tk.Radiobutton(janela, text="C++", variable=linguagem, value="C++")
rb1.pack()
rb2.pack()
rb3.pack()

# ---------- Exemplo 5: Scale ----------
scale_label = tk.Label(janela, text="Exemplo 5: Scale", font=("Arial", 12, "bold"))
scale_label.pack(pady=(20, 5))
valor_scale = tk.Scale(janela, from_=0, to=100, orient=tk.HORIZONTAL)
valor_scale.pack()

# ---------- Exemplo 6: ComboBox ----------
combo_label = tk.Label(janela, text="Exemplo 6: Combobox", font=("Arial", 12, "bold"))
combo_label.pack(pady=(20, 5))
lista_opcoes = ["Python", "Tkinter", "Java", "HTML"]
combo = ttk.Combobox(janela, values=lista_opcoes)
combo.set("Tkinter")
combo.pack()

# ---------- Exemplo 7: Botão com mensagem ----------

def mostrar_mensagem():
    messagebox.showinfo("Mensagem", f"Você escolheu {linguagem.get()} e {combo.get()}")

botao_msg = tk.Button(janela, text="Mostrar mensagem", command=mostrar_mensagem, bg="green", fg="white")
botao_msg.pack(pady=15)

janela.mainloop()
```

Esse exemplo mostra, em uma única janela, como vários widgets funcionam juntos e como você pode montar uma interface prática usando Tkinter.

---

Se quiser, posso fazer um segundo arquivo com uma versão ainda mais didática, em formato de apostila, ou um projeto guiado passo a passo para criar uma calculadora, formulário ou menu interativo em Tkinter.


## 8. Menus

Podemos criar menus na janela principal com `Menu`.

```python
menu_principal = tk.Menu(janela)
janela.config(menu=menu_principal)

arquivo = tk.Menu(menu_principal, tearoff=0)
arquivo.add_command(label="Abrir")
arquivo.add_command(label="Salvar")
arquivo.add_separator()
arquivo.add_command(label="Sair")

menu_principal.add_cascade(label="Arquivo", menu=arquivo)
```

## 9. Mensagens e diálogos

Tkinter também oferece caixas de diálogo.

### messagebox

```python
from tkinter import messagebox

messagebox.showinfo("Informação", "Tudo certo!")
messagebox.showwarning("Atenção", "Cuidado!")
messagebox.showerror("Erro", "Algo deu errado")
```

### filedialog
Permite abrir ou salvar arquivos.

```python
from tkinter import filedialog

arquivo = filedialog.askopenfilename()
print(arquivo)
```

## 10. Temas e estilo com ttk

A biblioteca `ttk` oferece widgets com aparência mais moderna.

Exemplo:

```python
from tkinter import ttk

botao = ttk.Button(janela, text="Botão estilo ttk")
botao.pack()
```

Widgets comuns de `ttk`:
- `Button`
- `Label`
- `Entry`
- `Combobox`
- `Checkbutton`
- `Radiobutton`
- `Treeview`
- `Progressbar`

## 11. Combobox

Cria uma caixa com lista de opções selecionáveis.

```python
valores = ["Python", "Java", "C++"]
combo = ttk.Combobox(janela, values=valores)
combo.pack()
```

## 12. Treeview

Permite criar tabelas e visualizações em árvore.

```python
arvore = ttk.Treeview(janela)
arvore["columns"] = ("nome", "idade")
arvore.heading("nome", text="Nome")
arvore.heading("idade", text="Idade")
arvore.insert("", "end", values=("Ana", 20))
arvore.pack()
```

## 13. Configuração da janela

Algumas propriedades básicas da janela principal:

```python
janela.title("Título da janela")
janela.geometry("500x300")
janela.resizable(width=False, height=False)
janela.iconbitmap("icone.ico")
```

### `title()`
Define o nome da janela.

### `geometry()`
Define tamanho inicial da janela.

### `resizable()`
Permite ou bloqueia redimensionamento.

## 14. Loop principal da interface

A função `mainloop()` é o coração do Tkinter. Ela fica em execução e mantém a interface responsiva, capturando eventos e atualizando os widgets.

```python
janela.mainloop()
```

Sem esse comando, a janela pode abrir e fechar rapidamente.

## 15. Exemplo completo de aplicação simples

```python
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
```

## 16. Boas práticas

- use `grid()` para layouts mais organizados;
- evite misturar muitas técnicas de posicionamento na mesma interface;
- nomeie funções de eventos com clareza;
- mantenha a lógica do programa separada da interface;
- use `ttk` quando quiser uma aparência mais moderna;
- sempre chame `mainloop()` ao final do programa.

## 17. Resumo

Tkinter é a forma mais direta de criar interfaces gráficas em Python. Os principais conceitos são:

- janela principal (`Tk`);
- widgets;
- geometria (`pack`, `grid`, `place`);
- eventos e callbacks;
- variáveis (`StringVar`, `IntVar`, etc.);
- menus e diálogos;
- `ttk` para widgets mais modernos;
- `mainloop()` para manter a janela em execução.

Com esses conceitos, você já consegue criar aplicações simples e úteis em Python com interface gráfica.

## 18. Próximos passos

Se quiser seguir aprendendo, vale estudar:
- criação de formulários;
- gerenciamento de eventos;
- uso de imagens em `Label`;
- criação de interfaces com `grid()`;
- projetos completos com Tkinter e banco de dados.

---

Se quiser, também posso criar um segundo documento com exercícios práticos de Tkinter ou um mini projeto completo usando `tkinter`.
