import base64
import hashlib
from geracao_em import cria_EM 


# receber a  mensagem
def encriptacao_rsapss(text: str, private_key):
# calcular hash da mensagem
    hash_text = hash(text)
# calcular EM
    em = cria_EM(hash_text)
#obter valores de EM, expoente e d
    emVal = int.from_bytes(em, byteorder='big', signed=False)
    dVal = int.from_bytes(private_key[0], byteorder='big', signed=False)
    nVal = int.from_bytes(private_key[1], byteorder='big', signed=False)
# criptografar
    S = pow(emVal, dVal, nVal)

    pass

def hash(text):
    encoded_text = text.encode("ascii")

    hasher = hashlib.sha3_256()

    hasher.update(encoded_text)
    hash_hex = hasher.hexdigest()
    hash_bytes = hasher.digest()
    # hash de 32 bytes
    return (hash_hex, hash_bytes) # retorno em hexadecimal