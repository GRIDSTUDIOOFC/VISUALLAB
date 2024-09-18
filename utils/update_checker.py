import requests
import os
import sys
import shutil

# URL do repositório e arquivo de release
REPO_URL = "https://api.github.com/repos/GRIDSTUDIOOFC/VISUALLAB/releases/latest"
DOWNLOAD_URL = "https://github.com/GRIDSTUDIOOFC/VISUALLAB/releases/download/{tag}/VISUALLAB.exe"

# Caminho para o arquivo executável
CURRENT_VERSION_FILE = "version.txt"
EXE_FILE = "ModernImageProcessorApp.exe"

def check_for_update():
    try:
        # Obter informações da versão mais recente
        response = requests.get(REPO_URL)
        response.raise_for_status()
        latest_release = response.json()
        latest_tag = latest_release["tag_name"]

        # Ler a versão atual
        if os.path.exists(CURRENT_VERSION_FILE):
            with open(CURRENT_VERSION_FILE, "r") as file:
                current_version = file.read().strip()
        else:
            current_version = "0.0.0"

        # Verificar se há uma atualização disponível
        if latest_tag > current_version:
            print(f"Nova versão disponível: {latest_tag}. Atualizando...")
            download_and_update(latest_tag)
        else:
            print("Você já está usando a versão mais recente.")
    except Exception as e:
        print(f"Erro ao verificar atualizações: {e}")

def download_and_update(tag):
    try:
        # URL para download do novo executável
        url = DOWNLOAD_URL.format(tag=tag)
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Salvar o novo arquivo
        temp_file = "update_temp.exe"
        with open(temp_file, "wb") as file:
            shutil.copyfileobj(response.raw, file)

        # Substituir o executável atual
        if os.path.exists(EXE_FILE):
            os.remove(EXE_FILE)
        shutil.move(temp_file, EXE_FILE)

        # Atualizar a versão
        with open(CURRENT_VERSION_FILE, "w") as file:
            file.write(tag)

        print("Atualização concluída. Reinicie o aplicativo.")
        sys.exit(0)
    except Exception as e:
        print(f"Erro ao atualizar o aplicativo: {e}")

if __name__ == "__main__":
    check_for_update()
