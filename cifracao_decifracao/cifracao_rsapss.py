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
