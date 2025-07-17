import base64
import hashlib
import re
from geracao_em import cria_EM 

def decriptacao_rsapss(signature: str):

    sign = signature.encode('ascii')
    a = base64.b64decode(sign)
    S = int.from_bytes(bytes=a, byteorder='big', signed=False)
    public_key_str = get_chave("public_key.pem")
    public_key = get_key_data(public_key_str)
    if public_key is None:
        return
    eVal = int(public_key[0])
    nVal = int(public_key[1])

    EM = pow(S, eVal, nVal)

    byte_len = (EM.bit_length() + 7) // 8
    byte_signature = EM.to_bytes(byteorder='big', length=byte_len,signed=False)
    byte_signature = b'\x00' + byte_signature
    b64_signature = base64.b64encode(byte_signature)
    em = b64_signature.decode('ascii')

    return em    

    
    # print('Decript em:', b64_signature)
    

# receber a  mensagem
def encriptacao_rsapss(text: str):
    private_key_str = get_chave("private_key.pem")
    private_key = get_key_data(private_key_str)
    if private_key is None:
        return 'error'
# calcular hash da mensagem
    hash_text = hash(text)
# calcular EM
    em = cria_EM(hash_text)
    print("a", em)
   
#obter valores de EM, expoente e d
    emVal = int.from_bytes(em, byteorder='big', signed=False)
    dVal = int(private_key[0])
    nVal = int(private_key[1])
# criptografar
    S = pow(emVal, dVal, nVal)

# Converter o número para bytes (big-endian)
    byte_len = (S.bit_length() + 7) // 8
    byte_signature = S.to_bytes(byteorder='big', length=byte_len,signed=False)
    b64_signature = base64.b64encode(byte_signature)
    signature = b64_signature.decode('ascii')
    return signature

def hash(text):
    encoded_text = text.encode("ascii")

    hasher = hashlib.sha3_256()

    hasher.update(encoded_text)
    hash_hex = hasher.hexdigest()
    hash_bytes = hasher.digest()
    # hash de 32 bytes
    return (hash_hex, hash_bytes) # retorno em hexadecimal

def get_chave(path):
    with open(path, 'r') as file:
        lines = file.readlines()
        lines = lines[1:-1]
        # for i in range(len(lines)):
        #     lines[i] = lines[i][:-2]
        key = ''.join(line for line in lines)
        return key
def  get_key_data(text):
    data = base64.b64decode(text)
    data = data.decode('ascii')
    # data = "modulo: 1\nexpoente: 2"
    
    match = re.search(r"modulo:\s*(\d+)\s*expoente:\s*(\d+)", data)
    
    if match:
        modulo = match.group(1)
        expoente = match.group(2)
        return((expoente, modulo))
    return None
    

text = "oi"
decriptacao_rsapss(encriptacao_rsapss(text))