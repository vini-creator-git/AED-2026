import tkinter as tk
from tkinter import messagebox, ttk
from random import choice


bases = {"A": "T", "T": "A", "C": "G", "G": "C"}
rnab = {"A": "U", "T": "A", "C": "G", "G": "C"}


class DNApiceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DNApice - Gerador de DNA e RNA")
        self.geometry("620x560")
        self.minsize(500, 420)

        self.quantidade = tk.StringVar(value="10")
        self.gerar_rna = tk.BooleanVar(value=False)

        self._criar_interface()

    def _criar_interface(self):
        principal = ttk.Frame(self, padding=16)
        principal.pack(fill="both", expand=True)

        ttk.Label(
            principal,
            text="DNApice",
            font=("TkDefaultFont", 18, "bold"),
        ).pack()
        ttk.Label(
            principal,
            text="Gerador de DNA e RNA",
        ).pack(pady=(0, 14))

        controles = ttk.LabelFrame(principal, text="Configurações", padding=10)
        controles.pack(fill="x")

        ttk.Label(controles, text="Quantidade de bases:").grid(
            row=0, column=0, sticky="w"
        )
        campo_quantidade = ttk.Entry(
            controles,
            textvariable=self.quantidade,
            width=12,
        )
        campo_quantidade.grid(row=0, column=1, padx=(8, 16), sticky="w")
        campo_quantidade.bind("<Return>", lambda _: self.gerar())

        ttk.Checkbutton(
            controles,
            text="Mostrar fita de RNA",
            variable=self.gerar_rna,
        ).grid(row=0, column=2, sticky="w")

        ttk.Button(
            controles,
            text="Gerar",
            command=self.gerar,
        ).grid(row=0, column=3, padx=(16, 0))

        self.saida = tk.Text(
            principal,
            height=20,
            wrap="none",
            state="disabled",
            font=("Consolas", 11),
        )
        self.saida.pack(fill="both", expand=True, pady=(14, 0))

        barra = ttk.Scrollbar(
            principal,
            orient="vertical",
            command=self.saida.yview,
        )
        barra.place(relx=1, rely=0.19, relheight=0.74, anchor="ne")
        self.saida.configure(yscrollcommand=barra.set)

        barra_horizontal = ttk.Scrollbar(
            principal,
            orient="horizontal",
            command=self.saida.xview,
        )
        barra_horizontal.pack(fill="x")
        self.saida.configure(xscrollcommand=barra_horizontal.set)

        self.saida.tag_configure("A", foreground="#c62828")
        self.saida.tag_configure("T", foreground="#8e24aa")
        self.saida.tag_configure("C", foreground="#2e7d32")
        self.saida.tag_configure("G", foreground="#00838f")
        self.saida.tag_configure("U", foreground="#8e24aa")
        self.saida.tag_configure(
            "ponte_at",
            foreground="#ef6c00",
            font=("Consolas", 11, "bold"),
        )
        self.saida.tag_configure(
            "ponte_cg",
            foreground="#1565c0",
            font=("Consolas", 11, "bold"),
        )
        self.saida.tag_configure(
            "orientacao",
            foreground="#6a1b9a",
            font=("Consolas", 11, "bold"),
        )
        self.saida.tag_configure("fita", justify="center", spacing1=2, spacing3=2)
        self.saida.tag_configure(
            "titulo",
            justify="center",
            foreground="#283593",
            font=("Consolas", 12, "bold"),
            spacing1=8,
            spacing3=5,
        )

    def _adicionar_base(self, base):
        self.saida.insert("end", base, base)
        self.saida.insert("end", " ")

    def _adicionar_fita_dupla(self, titulo, fita_superior, fita_inferior):
        self.saida.configure(state="normal")
        self.saida.insert("end", f"\n{titulo}\n", "titulo")
        self.saida.insert("end", "5' - ", "orientacao")
        for base in fita_superior:
            self._adicionar_base(base)
        self.saida.insert("end", "- 3'\n", "orientacao")

        self.saida.insert("end", "     ")
        for superior in fita_superior:
            tag = "ponte_at" if superior in ("A", "T") else "ponte_cg"
            self.saida.insert("end", "= " if tag == "ponte_at" else "≡ ", tag)

        self.saida.insert("end", "\n3' - ", "orientacao")
        for base in fita_inferior:
            self._adicionar_base(base)
        self.saida.insert("end", "- 5'\n", "orientacao")
        self.saida.configure(state="disabled")

    def _limpar_saida(self):
        self.saida.configure(state="normal")
        self.saida.delete("1.0", "end")
        self.saida.configure(state="disabled")

    def gerar(self):
        try:
            quant = int(self.quantidade.get())
        except ValueError:
            messagebox.showerror(
                "Quantidade inválida",
                "Informe um número inteiro de bases.",
            )
            return

        if quant <= 0:
            messagebox.showerror(
                "Quantidade inválida",
                "A quantidade deve ser maior que zero.",
            )
            return

        fita_dna = [choice(list(bases)) for _ in range(quant)]
        self._limpar_saida()

        fita_dna_superior = "".join(fita_dna)
        fita_dna_inferior = "".join(bases[base] for base in fita_dna)
        self._adicionar_fita_dupla(
            "FITA DE DNA",
            fita_dna_superior,
            fita_dna_inferior,
        )

        if self.gerar_rna.get():
            fita_rna = "".join(rnab[base] for base in fita_dna)
            self._adicionar_fita_dupla(
                "FITA DE RNA",
                fita_dna_superior,
                fita_rna,
            )

        self.saida.configure(state="normal")
        self.saida.see("end")
        self.saida.configure(state="disabled")


if __name__ == "__main__":
    app = DNApiceApp()
    app.mainloop()
