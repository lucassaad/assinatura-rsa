from pss.pss_padding import cria_EM
from utils.utils_rsapss import *

# receber a  mensagem
def encriptacao_rsapss(em_mensagem: bytes) -> bytes:
    private_key_str = get_key("private_key.pem")
    private_key = get_key_data(private_key_str)
    if private_key is None:
        raise OSError("Erro ao processar chave privada")
   
    # converter Em para inteiro
    emVal = int.from_bytes(em_mensagem, byteorder='big', signed=False)

    dVal = int(private_key[0])
    nVal = int(private_key[1])

    # calcular assinatura
    S = pow(emVal, dVal, nVal)

    # Converter assinatura para bytes (big-endian)
    key_len = (nVal.bit_length() + 7) // 8
    byte_signature = S.to_bytes(byteorder='big', length=key_len,signed=False)

    # codificar em base64 e retornar
    b64_signature = base64.b64encode(byte_signature)
    return b64_signature


from utils.utils_rsapss import *
 
def decriptacao_rsapss(assinatura: str) -> bytes:

    # assinatura_b64 = assinatura.encode('ascii')
    assinatura_bytes  = base64.b64decode(assinatura)
    assinatura_int = int.from_bytes(bytes=assinatura_bytes, byteorder='big', signed=False)
    public_key_b64 = get_key("public_key.pem")
    public_key = get_key_data(public_key_b64)
    if public_key is None:
        raise OSError("Erro ao processar chave") 
    eVal = int(public_key[0])
    nVal = int(public_key[1])

    EM = pow(assinatura_int, eVal, nVal)
    

    key_len = (nVal.bit_length() + 7) // 8
    em_assinatura_bytes = EM.to_bytes(byteorder='big', length=key_len,signed=False)

    # em_assinatura_bytes = b'\x00' + em_assinatura_bytes
    em_assinatura_b64 = base64.b64encode(em_assinatura_bytes)

    
    return em_assinatura_bytes    


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



import base64
from utils.utils_rsapss import get_hash
from cifracao_decifracao.decifracao_rsapss import decriptacao_rsapss

def verifica_assinatura(data: dict[str, str]) -> bool:
    mensagem = data["mensagem"]
    assinatura_b64 = data["assinatura"]  # já é str

    em_bytes = decriptacao_rsapss(assinatura_b64)  # passa str base64

    hash_extraido = extrai_hash_de_em(em_bytes)
    hash_mensagem = get_hash(mensagem)

    print({
        "hash_extraido": hash_extraido.hex(),
        "hash_mensagem": hash_mensagem.hex()
    })

    return hash_extraido == hash_mensagem

def extrai_hash_de_em(em_bytes: bytes, hash_len: int = 32, salt_len: int = 32) -> bytes:
    # Ajuste conforme a estrutura do seu EM
    total_len = len(em_bytes)
    ps_len = total_len - 1 - 1 - 1 - hash_len - salt_len  # [0x00, 0x01, PS, 0x00, hash, salt]
    start = 2 + ps_len + 1
    end = start + hash_len
    return em_bytes[start:end]