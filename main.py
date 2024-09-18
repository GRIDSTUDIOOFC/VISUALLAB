import tkinter as tk
from utils.update_checker import check_for_update
from utils.image_processing import adicionar_texto_imagem, extrair_descricao_antes_espaco, salvar_em_arquivo
from utils.file_operations import selecionar_pasta, listar_imagens, confirmar_processamento, exibir_dialogo_confirmacao

class ModernImageProcessorApp(tkb.Window):
    def __init__(self):
        super().__init__()
        self.title("Processador de Imagens")
        self.geometry("1200x800")
        self.resizable(False, False)
        self.configure(bg="#f4f6f9")

        self.font_size_var = tk.IntVar(value=4)
        self.font_color_var = tk.StringVar(value="#ff5733")
        self.current_image = None
        self.current_image_path = None
        self.history = []
        self.current_folder_path = None
        self.image_queue = queue.Queue()

        self.create_widgets()
        check_for_update()  # Check for updates on startup

    def create_widgets(self):
        # The widget creation code remains unchanged
        pass

    def processar_pasta_para_confirmacao(self, caminho_pasta):
        self.current_folder_path = caminho_pasta
        listar_imagens(caminho_pasta, self)

    def confirmar_processamento(self):
        confirmar_processamento(self, self.current_folder_path)

    def exibir_dialogo_confirmacao(self):
        exibir_dialogo_confirmacao(self)

if __name__ == "__main__":
    app = ModernImageProcessorApp()
    app.mainloop()
