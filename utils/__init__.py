# utils/__init__.py

# Importar funções e classes dos módulos
from .image_processing import adicionar_texto_imagem
from .file_operations import extrair_descricao_antes_espaco, salvar_em_arquivo
from .update_checker import check_for_updates

# Opcional: Definir o que será exportado quando o pacote for importado
__all__ = [
    'adicionar_texto_imagem',
    'extrair_descricao_antes_espaco',
    'salvar_em_arquivo',
    'check_for_updates'
]

# Mensagem de inicialização opcional
print("Pacote utils importado e inicializado.")
