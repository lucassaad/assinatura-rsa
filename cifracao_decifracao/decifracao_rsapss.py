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