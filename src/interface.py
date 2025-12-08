import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("Trabalho de Inteligência Artificial (Sistema Especialista) – Luzes do Painel de Carros")

        self.imagem = Image.open("interface.jpg")
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

        # x += 125 y += 70
        self.regioes = {
            "bateria":            (200, 340, 255, 385),
            "oleo":               (65, 270, 150, 315),
            "temperatura":        (900, 330, 950, 380),
            "freio":              (290, 80, 375, 150),
            "cinto":              (865, 260, 920, 310),
            "combustivel-baixo":  (770, 335, 810, 380),
            "flex":               (450, 205, 545, 265),
            "airbag":             (190, 280, 235, 325),
            "farol-alto":         (40, 340, 100, 385),
            "seta":               (445, 80, 555, 155),
            "porta":              (800, 265, 840, 315),
            "freio-mao":          (625, 85, 710, 150)
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
        self.master.event_generate("<<EscolhaConcluida>>")

    # Mostra caixa de pergunta com botões
    def perguntar(self, texto, opcoes):
        janela = tk.Toplevel(self.master)
        janela.title("Pergunta")

        # --- Widgets ---
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

        # --- Centralizar a janela ---
        janela.update_idletasks()  # Atualiza tamanho da janela

        largura = janela.winfo_width()
        altura = janela.winfo_height()

        # Tamanho da tela
        largura_tela = self.master.winfo_width()
        altura_tela = self.master.winfo_height()

        # Cálculo da posição
        x = self.master.winfo_x() + (largura_tela // 2) - (largura // 2)
        y = self.master.winfo_y() + (altura_tela // 2) - (altura // 2)

        janela.geometry(f"{largura}x{altura}+{x}+{y}")

        # --- Modal ---
        janela.grab_set()
        janela.wait_window()
        return resposta["valor"]

    # Mostra o resultado
    def mostrar(self, texto):
        messagebox.showinfo("Resultado", texto)

    # Para mapear as coordenadas
    def _click_coordenadas(self, event):
        print(f"\nClique em: X={event.x}, Y={event.y}")
