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

