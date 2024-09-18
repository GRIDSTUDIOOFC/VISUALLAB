# utils/file_operations.py

import os

def extrair_descricao_antes_espaco(caminho_pasta):
    """
    Extrai a descrição dos arquivos de imagem, que é a parte antes do primeiro espaço no nome do arquivo.
    """
    descricoes = []
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            descricao = arquivo.split(" ")[0]
            descricoes.append((arquivo, descricao))
    return descricoes

def salvar_em_arquivo(descricoes, caminho_pasta):
    """
    Salva as descrições extraídas em um arquivo de texto na pasta especificada.
    """
    try:
        with open(os.path.join(caminho_pasta, "descricoes.txt"), "w") as arquivo:
            for _, descricao in descricoes:
                arquivo.write(f"{descricao}\n")
    except Exception as e:
        print(f"Erro ao salvar descrições em arquivo: {e}")
