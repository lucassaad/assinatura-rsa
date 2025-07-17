from geracao_serializacao.geracao_chaves import geracao_chaves_rsa
from utils.utils_rsapss import get_hash
from geracao_serializacao.serializacao_armazenamento import serializa_chave, armazena_chave
from pss.pss_padding import cria_EM
from cifracao_decifracao.cifracao_rsapss import encriptacao_rsapss
from verificacao.verificar_assinatura import verifica_assinatura

import base64



if __name__ == "__main__":
    mensagem = input("Mensagem a ser assinada: ")
    chaves = geracao_chaves_rsa(1024)
    chaves_serializadas = serializa_chave(chaves)
    print("Chaves serializadas (Base64): ", chaves_serializadas)
    print()
    armazena_chave(chaves_serializadas)

    hashed_mensagem = get_hash(mensagem)
    em_mensagem = cria_EM(hashed_mensagem)
    print("EM: ", base64.b64encode(em_mensagem))
    print()

    # Assinatura (retorna bytes base64)
    assinatura_b64 = encriptacao_rsapss(em_mensagem)
    print("Assinatura (base64): ", assinatura_b64)
    print()

    # Monta o dicionário para verificação (assinatura como string base64)
    mensagem_assinada = {
        #"mensagem": mensagem + "a",
        "mensagem": mensagem,
        "assinatura": assinatura_b64.decode()  # converte bytes base64 para string base64
    }
    print('Mensagem assinada: ', mensagem_assinada)

    # Verificação da assinatura
    resultado = verifica_assinatura(mensagem_assinada)
    print("Assinatura válida?", resultado)

    