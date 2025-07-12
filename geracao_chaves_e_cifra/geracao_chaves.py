import random
from geracao_primo import geracao_num_primo

BITS_CHAVE = 1024

def get_primos(num_bits):
    first = geracao_num_primo(num_bits)
    second = geracao_num_primo(num_bits)
    return (first, second)

def get_mdc(a, b):
    while b:
        a, b = b, a % b
    return a

def get_expoente_publico(k):
    while True:
        e = random.randrange(2, k)
        mdc = get_mdc(e, k)
        if mdc == 1:
            return e

def get_expoente_privado(k, e):
    d = pow(e, -1, k)
    return d

def geracao_chaves_rsa(num_bits):
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
