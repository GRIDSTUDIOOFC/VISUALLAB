import os
import threading
import time
import queue
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttkb

def selecionar_pasta(app):
    try:
        caminho_pasta = filedialog.askdirectory(title="Selecione a Pasta")
        if caminho_pasta:
            app.processar_pasta_para_confirmacao(caminho_pasta)
    except Exception as e:
        print(f"Erro ao selecionar pasta: {e}")

def listar_imagens(caminho_pasta, app):
    try:
        for widget in app.canvas_frame_content.winfo_children():
            widget.destroy()
        app.canvas_images.clear()
        app.image_queue.queue.clear()
        threading.Thread(target=load_images, args=(caminho_pasta, app)).start()
    except Exception as e:
        print(f"Erro ao listar imagens: {e}")

def load_images(caminho_pasta, app):
    try:
        col = 0
        row = 0
        for arquivo in os.listdir(caminho_pasta):
            if arquivo.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                caminho_imagem = os.path.join(caminho_pasta, arquivo)
                img = Image.open(caminho_imagem)
                img.thumbnail((150, 150))
                img_tk = ImageTk.PhotoImage(img)
                app.image_queue.put((img_tk, row, col))
                if app.image_queue.qsize() > 0:
                    img_tk, row, col = app.image_queue.get()
                    label = ttkb.Label(app.canvas_frame_content, image=img_tk)
                    label.image = img_tk
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                    col += 1
                    if col > 4:
                        col = 0
                        row += 1
        app.canvas_frame_content.update_idletasks()
        app.canvas.config(scrollregion=app.canvas.bbox("all"))
    except Exception as e:
        print(f"Erro ao carregar imagens: {e}")

def confirmar_processamento(app, caminho_pasta):
    try:
        if not caminho_pasta:
            raise ValueError("Nenhuma pasta selecionada.")
            
        app.select_button.config(state=tk.DISABLED)
        app.status_label.config(text="Processando...", foreground="#333333")

        def atualizar_barra(progresso):
            app.progress_bar['value'] = progresso
            app.progress_percentage.config(text=f"{int(progresso)}%")

        def finalizar_processamento():
            app.status_label.config(text="Processamento Concluído!", foreground="#28a745")
            app.progress_bar['value'] = 100
            app.progress_percentage.config(text="100%")
            app.exibir_dialogo_confirmacao()

        def processo_em_background(caminho_pasta):
            try:
                descricoes = extrair_descricao_antes_espaco(caminho_pasta)
                salvar_em_arquivo(descricoes, caminho_pasta)
                
                total_tarefas = len(descricoes)
                progresso = 0
                
                for arquivo, descricao in descricoes:
                    caminho_imagem = os.path.join(caminho_pasta, arquivo)
                    if os.path.isfile(caminho_imagem):
                        adicionar_texto_imagem(caminho_imagem, descricao, app.font_size_var.get(), app.font_color_var.get())
                        progresso += 1
                        app.after(100, lambda p=progresso: atualizar_barra((p / total_tarefas) * 100))
                        time.sleep(0.1)

                app.history.append(caminho_pasta)
                app.after(100, finalizar_processamento)
            except Exception as e:
                app.after(100, lambda: app.status_label.config(text=f"Erro: {e}", foreground="#dc3545"))
                app.select_button.config(state=tk.NORMAL)
                print(f"Erro no processamento: {e}")

        threading.Thread(target=processo_em_background, args=(caminho_pasta,)).start()
    except Exception as e:
        print(f"Erro ao processar imagens: {e}")

def exibir_dialogo_confirmacao(app):
    try:
        if messagebox.askyesno("Processamento Concluído", "O processamento foi concluído com sucesso. Deseja processar outra pasta?"):
            app.select_button.config(state=tk.NORMAL)
        else:
            app.quit()
    except Exception as e:
        print(f"Erro ao exibir diálogo de confirmação: {e}")
