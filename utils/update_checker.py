# utils/update_checker.py

import requests

def check_for_update(current_version, repo_url):
    """
    Verifica se há uma nova versão do aplicativo disponível no repositório.
    """
    try:
        response = requests.get(f"{repo_url}/releases/latest")
        response.raise_for_status()
        latest_version = response.json().get("tag_name", "0.0.0")

        return latest_version > current_version
    except requests.RequestException as e:
        print(f"Erro ao verificar atualização: {e}")
        return False
