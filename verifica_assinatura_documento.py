import os
from utils.utils_rsapss import get_hash
from pss.pss_padding import cria_EM
from verificacao.verificar_assinatura import verifica_assinatura

def verificar_arquivo(caminho_arquivo: str, caminho_assinatura: str) -> bool:
    """
    Verifica a assinatura digital de um arquivo usando o arquivo .sig.
    Retorna True se a assinatura for válida, False caso contrário.
    """
    # Lê o arquivo original como bytes
    with open(caminho_arquivo, "rb") as f:
        conteudo = f.read()

    # Lê a assinatura (base64 string)
    with open(caminho_assinatura, "r") as f:
        assinatura_b64 = f.read().strip()

    # Monta o dicionário esperado pela função de verificação
    dados = {
        "mensagem": conteudo,  # get_hash já aceita bytes!
        "assinatura": assinatura_b64
    }

    # Verifica a assinatura
    return verifica_assinatura(dados)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    arquivos_sig = [f for f in os.listdir(script_dir) if f.endswith('.sig') and os.path.isfile(os.path.join(script_dir, f))]
    if not arquivos_sig:
        print("Nenhum arquivo .sig encontrado neste diretório.")
        exit(1)
    print("Arquivos de assinatura (.sig) disponíveis:")
    for idx, nome in enumerate(arquivos_sig, 1):
        print(f"{idx}. {nome}")
    while True:
        try:
            escolha = int(input("Escolha o número do arquivo .sig para verificar: "))
            if 1 <= escolha <= len(arquivos_sig):
                caminho_sig = os.path.join(script_dir, arquivos_sig[escolha-1])
                caminho = os.path.join(script_dir, arquivos_sig[escolha-1][:-4])
                break
            else:
                print("Escolha inválida. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")
    if not os.path.isfile(caminho):
        print(f"Arquivo original '{caminho}' não encontrado!")
    else:
        valido = verificar_arquivo(caminho, caminho_sig)
        if valido:
            print("Assinatura VÁLIDA para este arquivo!")
        else:
            print("Assinatura INVÁLIDA para este arquivo!")
