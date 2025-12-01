import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema Especialista – Luzes do Painel")

        self.imagem = Image.open("luzes_painel_carro.jpg")
        self.imgtk = ImageTk.PhotoImage(self.imagem)

        # Canvas para exibir a imagem
        self.canvas = tk.Canvas(master, width=self.imgtk.width(), height=self.imgtk.height())
        self.canvas.pack()

        # Desenha a imagem no canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.imgtk)

        # Para mapear as coordenadas das luzes da imagem
        # self.canvas.bind("<Button-1>", self._click_coordenadas) # <------------- Só descomentar

        # Onde será armazenada a escolha da luz
        self.escolha = None

        self.regioes = {
            "bateria":      (850, 110, 900, 150),
            "oleo":         (95, 260, 170, 305),
            "temperatura":  (470, 340, 520, 390),
            "freio":        (640, 190, 690, 230),
            "cinto":        (750, 110, 790, 150),
        }

        # Cria áreas invisíveis clicáveis
        self._criar_regioes_clicaveis()

    # Cria "retângulos invisíveis" que são regiões clicaveis na imagem
    def _criar_regioes_clicaveis(self):
        for nome, (x1, y1, x2, y2) in self.regioes.items():

            # Cria um "retângulo invisível"
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="",
                fill="",
                tags=nome
            )

            # Vincula o clique
            self.canvas.tag_bind(nome, "<Button-1>", lambda e, n=nome: self._selecionar(n))

    # Quando o usuário clica sobre uma região da imagem
    def _selecionar(self, valor):
        self.escolha = valor
        print(self.escolha)
        self.master.event_generate("<<EscolhaConcluida>>")

    # Mostra caixa de pergunta com botões
    def perguntar(self, texto, opcoes):
        janela = tk.Toplevel(self.master)
        janela.title("Pergunta")

        tk.Label(janela, text=texto, font=("Arial", 12)).pack(pady=10)

        resposta = {"valor": None}

        def escolher(v):
            resposta["valor"] = v
            janela.destroy()

        for op in opcoes:
            tk.Button(
                janela, text=op, font=("Arial", 11),
                command=lambda v=op: escolher(v)
            ).pack(pady=3, fill="x")

        janela.grab_set()
        janela.wait_window()
        return resposta["valor"]

    # Mostra o resultado
    def mostrar(self, texto):
        messagebox.showinfo("Resultado", texto)

    # Para mapear as coordenadas
    def _click_coordenadas(self, event):
        print(f"\nClique em: X={event.x}, Y={event.y}")
