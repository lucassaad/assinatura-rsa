# Rode este script a partir da raiz do projeto:
# python assintura_documentos/assinatura_documento.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import base64
from utils.utils_rsapss import get_hash
from pss.pss_padding import cria_EM
from cifracao_decifracao.cifracao_rsapss import encriptacao_rsapss

def assinar_arquivo(nome_arquivo: str) -> str:
    print(nome_arquivo)
    # Lê o arquivo como bytes
    with open(nome_arquivo, "rb") as f:
        conteudo = f.read()

    # Gera o hash e o EM
    hash_arquivo = get_hash(conteudo)  # Agora aceita bytes!
    em = cria_EM(hash_arquivo)

    # Gera a assinatura (em base64, tipo bytes)
    assinatura_b64 = encriptacao_rsapss(em)

    # Salva a assinatura em um arquivo separado (como base64 string)
    caminho_assinatura = nome_arquivo + ".sig"
    with open(caminho_assinatura, "w") as f:
        f.write(assinatura_b64.decode())

    print(f"Arquivo '{nome_arquivo}' assinado com sucesso.")
    print(f"Assinatura salva em: '{caminho_assinatura}'")
    return caminho_assinatura

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    arquivos = [f for f in os.listdir(script_dir) if os.path.isfile(os.path.join(script_dir, f)) and not f.endswith('.py') and not f.endswith('.pyc') and not f.endswith('.sig') and not f.endswith('.pem') and not f.endswith('.gitignore')]
    if not arquivos:
        print("Nenhum arquivo disponível para assinar neste diretório.")
        sys.exit(1)
    print("Arquivos disponíveis para assinar:")
    for idx, nome in enumerate(arquivos, 1):
        print(f"{idx}. {nome}")
    while True:
        try:
            escolha = int(input("Escolha o número do arquivo a ser assinado: "))
            if 1 <= escolha <= len(arquivos):
                file = os.path.join(script_dir, arquivos[escolha-1])
                break
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")
    assinar_arquivo(file)
