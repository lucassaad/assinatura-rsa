import random
from geracao_serializacao.geracao_primo import geracao_num_primo
from utils.utils_geracoes import get_mdc

BITS_CHAVE = 1024

def geracao_chaves_rsa(num_bits: int) -> tuple[tuple[int, int], tuple[int, int]]:
    # definir p e q
    p = geracao_num_primo(num_bits)
    q = geracao_num_primo(num_bits)
    while q == p:
        q = geracao_num_primo(num_bits)

    # definir n e phi_n
    n = p * q
    phi_n = (p-1)*(q-1)
    
    # definir expoente publico
    e = get_expoente_publico(phi_n)

    # definir expoente privado
    d = get_expoente_privado(phi_n, e)

    return ((e, n), (d, n))

# importante destacar o porque dessa escolha
def get_expoente_publico(phi_n: int):
    
    # Codigo para definir um "e" aleatorio
    # while True:
    #     e = random.randrange(2, phi_n)
    #     mdc = get_mdc(e, phi_n)
    #     if mdc == 1:
    #         return e

    # por padrão utiliza-se o expoente 65537
    # eficiente para calculo de m**e
    # seguro
    return 65537 
        
def get_expoente_privado(phi_n: int, expoente_pub: int) -> int:
    expoente_priv = pow(expoente_pub, -1, phi_n)
    return expoente_priv

