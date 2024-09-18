# main.py

import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import threading
import queue
import ttkbootstrap as ttkb
from utils import extrair_descricao_antes_espaco, salvar_em_arquivo, check_for_update

class ModernImageProcessorApp(ttkb.Window):
    def __init__(self):
        super().__init__()
        self.title("Processador de Imagens")
        self.geometry("1200x800")  # Tamanho fixo da janela principal
        self.resizable(False, False)  # Impede o redimensionamento da janela
        self.configure(bg="#f4f6f9")

        # Variáveis de configuração
        self.font_size_var = tk.IntVar(value=4)
        self.font_color_var = tk.StringVar(value="#ff5733")  # Cor hexadecimal para vermelho
        self.current_image = None
        self.current_image_path = None
        self.history = []
        self.current_folder_path = None
        self.image_queue = queue.Queue()  # Fila para gerenciar as imagens

        self.create_widgets()

    def create_widgets(self):
        try:
            # Main Frame
            self.main_frame = ttkb.Frame(self, padding=20)
            self.main_frame.pack(fill=tk.BOTH, expand=True)

            # Title
            self.title_label = ttkb.Label(self.main_frame, text="Processador de Imagens", 
                                          font=("Roboto", 28, "bold"), anchor="center")
            self.title_label.pack(pady=(0, 20))

            # Frame para o painel de configurações e visualização
            self.create_pane_frames()

            # Footer
            self.footer_label = ttkb.Label(self.main_frame, text="© 2024 Processador de Imagens", font=("Roboto", 10))
            self.footer_label.pack(side=tk.BOTTOM, pady=10)
        except Exception as e:
            print(f"Erro ao criar widgets: {e}")

    def create_pane_frames(self):
        try:
            # Frame de Configurações
            self.settings_frame = ttkb.LabelFrame(self.main_frame, text="Configurações", 
                                                  bootstyle="info", padding=(20, 20))
            self.settings_frame.pack(pady=20, padx=10, side=tk.LEFT, anchor='nw', fill=tk.Y)

            # Definindo a largura e altura fixa para o painel de configurações
            self.settings_frame.config(width=300, height=600)

            # Configura o layout do painel de configurações
            self.settings_frame.grid_columnconfigure(0, weight=1)
            self.settings_frame.grid_columnconfigure(1, weight=1)
            self.settings_frame.grid_rowconfigure(0, weight=0)
            self.settings_frame.grid_rowconfigure(1, weight=0)
            self.settings_frame.grid_rowconfigure(2, weight=0)
            self.settings_frame.grid_rowconfigure(3, weight=0)  # Linha para o botão de confirmação
            self.settings_frame.grid_rowconfigure(4, weight=0)  # Linha para a barra de progresso
            self.settings_frame.grid_rowconfigure(5, weight=1)  # Linha para status

            ttkb.Label(self.settings_frame, text="Tamanho da Fonte:").grid(row=0, column=0, padx=10, pady=(10, 0), sticky=tk.W)
            font_size_scale = ttkb.Scale(self.settings_frame, from_=1, to=10, variable=self.font_size_var, command=self.update_preview, orient="horizontal")
            font_size_scale.grid(row=0, column=1, pady=(10, 0), sticky="ew")
            self.font_size_label = ttkb.Label(self.settings_frame, text=self.font_size_var.get())
            self.font_size_label.grid(row=0, column=2, padx=10, pady=(10, 0))

            # Atualizar a numeração da escala
            self.font_size_var.trace("w", self.update_font_size_label)

            ttkb.Label(self.settings_frame, text="Cor do Texto:").grid(row=1, column=0, padx=10, pady=(10, 0), sticky=tk.W)

            # Botão de escolher cor
            self.color_button = ttkb.Button(self.settings_frame, text="Escolher Cor", command=self.choose_color, bootstyle="primary", width=20)
            self.color_button.grid(row=1, column=1, padx=10, pady=5, sticky="n")

            # Botão de confirmação
            self.confirm_button = ttkb.Button(self.settings_frame, text="Confirmar", command=self.confirmar_processamento, bootstyle="success", width=20)
            self.confirm_button.grid(row=3, column=0, columnspan=2, pady=(10, 0))

            # Botão para selecionar a pasta
            self.select_button = ttkb.Button(self.settings_frame, text="Escolher Pasta", command=self.selecionar_pasta, bootstyle="info", width=20)
            self.select_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))

            # Barra de progresso
            self.progress_bar = ttkb.Progressbar(self.settings_frame, orient="horizontal", length=250, mode="determinate")
            self.progress_bar.grid(row=4, column=0, columnspan=2, pady=(10, 5))

            self.progress_percentage = ttkb.Label(self.settings_frame, text="0%")
            self.progress_percentage.grid(row=5, column=0, columnspan=2, pady=(5, 10))

            self.status_label = ttkb.Label(self.settings_frame, text="", font=("Roboto", 12))
            self.status_label.grid(row=6, column=0, columnspan=2, pady=(10, 10))

            # Frame de Visualização de Imagens
            self.create_image_display_frame()

        except Exception as e:
            print(f"Erro ao criar frames: {e}")

    def create_image_display_frame(self):
        try:
            # Frame for image display with fixed width and height
            self.canvas_frame = ttkb.Frame(self.main_frame, width=1000, height=400)  # Ajustado para acomodar 5 imagens
            self.canvas_frame.pack(pady=20, fill=tk.BOTH, side=tk.RIGHT, anchor='ne')

            # Definir a largura e altura fixa para o painel de visualização de imagens
            self.canvas_frame.config(width=1000, height=400)

            # Canvas com barra de rolagem horizontal e vertical
            self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=1000, height=400)
            self.scroll_x = ttkb.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
            self.scroll_y = ttkb.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
            self.canvas.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
            self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Frame de Controles das Imagens
            self.controls_frame = ttkb.Frame(self.canvas_frame)
            self.controls_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)

            # Botão para adicionar imagem
            self.add_image_button = ttkb.Button(self.controls_frame, text="Adicionar Imagem", command=self.adicionar_imagem, bootstyle="primary", width=20)
            self.add_image_button.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"Erro ao criar o frame de visualização de imagens: {e}")

    def choose_color(self):
        try:
            color_code = colorchooser.askcolor(title="Escolha a Cor do Texto")[1]
            if color_code:
                self.font_color_var.set(color_code)
                self.update_preview()
        except Exception as e:
            print(f"Erro ao escolher a cor: {e}")

    def update_font_size_label(self, *args):
        try:
            self.font_size_label.config(text=self.font_size_var.get())
            self.update_preview()
        except Exception as e:
            print(f"Erro ao atualizar o tamanho da fonte: {e}")

    def update_preview(self, *args):
        try:
            font_size = self.font_size_var.get()
            font_color = self.font_color_var.get()
            self.preview_label.config(font=("Arial", font_size), foreground=font_color)
        except Exception as e:
            print(f"Erro ao atualizar a pré-visualização: {e}")

    def adicionar_imagem(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Arquivos de Imagem", "*.jpg;*.jpeg;*.png;*.bmp")])
            if file_path:
                image = Image.open(file_path)
                photo = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.canvas.image = photo  # Manter uma referência para evitar que a imagem seja removida
                self.current_image_path = file_path
                self.current_image = image
        except Exception as e:
            print(f"Erro ao adicionar imagem: {e}")

    def selecionar_pasta(self):
        try:
            self.current_folder_path = filedialog.askdirectory()
            if self.current_folder_path:
                descricoes = extrair_descricao_antes_espaco(self.current_folder_path)
                salvar_em_arquivo(descricoes, self.current_folder_path)
                self.status_label.config(text="Descrição das imagens salva com sucesso!")
        except Exception as e:
            print(f"Erro ao selecionar pasta: {e}")

    def confirmar_processamento(self):
        try:
            # Simulação do processamento
            self.status_label.config(text="Processando...")
            for i in range(101):
                time.sleep(0.05)
                self.progress_bar["value"] = i
                self.progress_percentage.config(text=f"{i}%")
                self.update_idletasks()
            self.status_label.config(text="Processamento Concluído!")
        except Exception as e:
            print(f"Erro ao confirmar processamento: {e}")

if __name__ == "__main__":
    app = ModernImageProcessorApp()
    app.mainloop()
