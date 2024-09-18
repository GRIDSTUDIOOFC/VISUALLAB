from PIL import Image, ImageDraw, ImageFont

def adicionar_texto_imagem(caminho_imagem, descricao, tamanho_fonte, cor_fonte):
    try:
        imagem = Image.open(caminho_imagem)
        draw = ImageDraw.Draw(imagem)
        font_size = 42 + (tamanho_fonte - 1) * 2
        try:
            fonte = ImageFont.truetype("assets/arial.ttf", font_size)
        except IOError:
            fonte = ImageFont.load_default()

        formato_original = imagem.format
        
        if formato_original == 'JPEG':
            if imagem.mode != 'RGB':
                imagem = imagem.convert('RGB')

        bbox = draw.textbbox((0, 0), descricao, font=fonte)
        texto_largura = bbox[2] - bbox[0]
        texto_altura = bbox[3] - bbox[1]
        posicao = (10, imagem.height - texto_altura - 10)
        draw.text(posicao, descricao, font=fonte, fill=cor_fonte)

        dpi = imagem.info.get('dpi', (72, 72))

        if formato_original == 'JPEG':
            imagem.save(caminho_imagem, format='JPEG', quality=100, optimize=True, dpi=dpi)
        else:
            imagem.save(caminho_imagem, format=formato_original, optimize=True, dpi=dpi)
    except Exception as e:
        print(f"Erro ao adicionar texto na imagem {caminho_imagem}: {e}")

def extrair_descricao_antes_espaco(caminho_pasta):
    descricoes = []
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            descricao = arquivo.split(" ")[0]
            descricoes.append((arquivo, descricao))
    return descricoes

def salvar_em_arquivo(descricoes, caminho_pasta):
    try:
        with open(os.path.join(caminho_pasta, "descricoes.txt"), "w") as arquivo:
            for _, descricao in descricoes:
                arquivo.write(f"{descricao}\n")
    except Exception as e:
        print(f"Erro ao salvar descrições em arquivo: {e}")
