import hashlib
import os

def cria_EM(hash):
    # hash da mensagem: 32 bytes
    Hm = hash
    hLen = len(Hm[1]) # 32 bytes
    
    # gerar salt: mesmo tamanho do hash: 32 bytes
    Salt = salt(hLen)
    sLen = len(Salt)

    # total - bytes fixos - len(H(M)) - len(Salt)
    psLen = 189 # 256 - 1 - 1 - 1 - 32 - 32   
  
    # Crie a semente para MGF1: mgf_seed = H(M) || Salt.
    seed = Hm[1] + Salt
    ps = mgf(seed, psLen)    
    # print("Len PS:", len(ps))

    EM = b'\x00' + b'\x01' + ps + b'\x00' + Hm[1] + Salt
    # print(EM)
    return EM

def salt(num_bytes):
    return os.urandom(32) # num_bytes ja definidos para facilitacao do projeto


def mgf(mgf_seed, len_ps):
    ps = b''
    i = 0
    # Iteracao para gerar os blocos do PS:
    while len(ps) < len_ps:
        # Converta i para uma sequência de 4 bytes.
        counter = i.to_bytes(4, byteorder='big', signed=False)

        mgf_hash_input = mgf_seed + counter
        
        # Calcule current_hash_block
        hasher = hashlib.sha3_256()
        hasher.update(mgf_hash_input)
        current_hash_block = hasher.digest()

        # Concatene current_hash_block ao PS.
        ps = ps + current_hash_block
        i += 1
    # retorna os "len_ps" primeiros bytes de ps      
    return ps[:len_ps]