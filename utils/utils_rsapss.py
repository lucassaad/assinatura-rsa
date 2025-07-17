import hashlib
import base64
import re
# Faz o hash de uma string

def get_hash(data) -> bytes:
    if isinstance(data, str):
        encoded = data.encode("ascii")
    else:
        encoded = data
    hasher = hashlib.sha3_256()
    hasher.update(encoded)
    return hasher.digest()

    def get_hash(text: str) -> bytes:
        encoded_text = text.encode("ascii")

        hasher = hashlib.sha3_256()

        hasher.update(encoded_text)
        hash_bytes = hasher.digest()
        # hash de 32 bytes
        return hash_bytes # retorno em hexadecimal

# Pega a chave que esta no arquivo pem
def get_key(path: str) -> str:
    with open(path, 'r') as file:
        lines = file.readlines()
        lines = lines[1:-1]
        key = ''.join(line for line in lines)
        return key

# Pega dados da chave (expoente, modulo)    
def  get_key_data(text: str) -> tuple[str, str]: # type: ignore
    data = base64.b64decode(text)
    data = data.decode('ascii')
    
    match = re.search(r"modulo:\s*(\d+)\s*expoente:\s*(\d+)", data)
    
    if match is None:
        raise ValueError("Erro na recuperação da chave")
    if match:
        modulo = match.group(1)
        expoente = match.group(2)
        return((expoente, modulo))
        