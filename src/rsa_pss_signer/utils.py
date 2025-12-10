import hashlib
import base64
import re
import random

# Para isso escolheremos um numero entre:
#     - (2**1024) - 1: maior numero com 1024 bits
#     - (2**1023) + 1: menor numero com 1024 bits
def nBitRandom(num_bits):
    max_n_bit_num = 2**(num_bits) - 1
    min_n_bit_num = 2**(num_bits-1) + 1

    result = (random.randrange(min_n_bit_num, max_n_bit_num + 1))
    if result % 2 == 0:
        result += 1

    return result

def get_mdc(a, b):
    while b:
        a, b = b, a % b
    return a

# Faz o hash de uma string

def get_hash(data) -> bytes:
    if isinstance(data, str):
        encoded = data.encode("ascii")
    else:
        encoded = data
    hasher = hashlib.sha3_256()
    hasher.update(encoded)
    return hasher.digest()


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
        