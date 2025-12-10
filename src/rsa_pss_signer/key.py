import random
from geracao_serializacao.geracao_primo import geracao_num_primo
from utils.utils_geracoes import get_mdc



import random
from utils.utils_geracoes import nBitRandom
import base64

from geracao_serializacao.geracao_chaves import geracao_chaves_rsa

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



NUMBER_OF_RABIN_ROUNDS = 40
first_primes_list = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103,
    107, 109, 113, 127, 131, 137, 139,
    149, 151, 157, 163, 167, 173, 179,
    181, 191, 193, 197, 199, 211, 223,
    227, 229, 233, 239, 241, 251, 257,
    263, 269, 271, 277, 281, 283, 293,
   ]

# Geracao:
def geracao_num_primo(num_bits: int) -> int:
    while True:
        random_n_bit_number = nBitRandom(num_bits)
        lowLevelPrimality_result = lowPrimes_primalityTest(random_n_bit_number)
        if lowLevelPrimality_result:
            prime_number_result = millerRabin_primalityTest(random_n_bit_number)
            if prime_number_result: 
                return random_n_bit_number    

# Primeiro teste de primalidade:
# dividir pelos primeiros numeros primos 
# importancia: elimina previamente numeros compostos faceis de reconhecer
def lowPrimes_primalityTest(num: int) -> bool:
    for divisor in first_primes_list:
        if num % divisor == 0:
            return False
    return True     

# Miller Rabin
# teste deterministico para saber se um numero e primo ou não

def millerRabin_primalityTest(num: int) -> bool:
# primeira etapa:
# descobrir k e m em: num-1 = 2**k * m

    k  = 0 # k = max division by two 
    m = num - 1 # even component

    while m % 2 == 0:
        m >>= 1 # shift right == dividir por 2 
        k += 1 

    # repeticao do processo de conclusao do miller rabin para garantir assertividade   
    for _ in range(NUMBER_OF_RABIN_ROUNDS):        
    # segunda etapa:
    # escolher um numero "a", tal que
    # 1 < a < num
        a = random.randrange(2, num - 1)
        if (trialComposite(a, k, m, num)):
            return False
    return True   
         
def trialComposite(base:int, k: int, expoente: int, num: int) -> bool:
    # terceira etapa:
    # calcular b0 = a**m (mod num)
    # para b0: se b0 == 1 ou -1, num provavelmente primo
    # se b0 != 1 ou -1: calcular: b1 = b0**2 mod(num), e assim por diante
    # para b1,b2,..,bn: 1->composto, -1->primo 
        result = pow(base, expoente, num) # pow(base, expoente, modulo)
        if result == 1 or result == num - 1:
            return False
        else:
            for _ in range(k - 1):
                result = pow(result, 2, num)
                if result == 1:
                    return True
                elif result == num - 1:
                    return False
            return True    
        


def serializa_chave(chaves: tuple[tuple[int, int], tuple[int, int]]) -> tuple[str, str]:
    # chave publica
    public_key = chaves[0]
    pubK_str = cria_key_string(public_key)
    # chave privada
    private_key = chaves[1]
    privK_str = cria_key_string(private_key)

    # str para bytes
    pubK_bytes = pubK_str.encode('ascii')
    privK_bytes = privK_str.encode('ascii')

    # bytes para base64
    pubK_base64 = base64.b64encode(pubK_bytes).decode('ascii')
    privK_base64 = base64.b64encode(privK_bytes).decode('ascii')
    
    # cria o conteudo para colocar no arquivo pem
    
    return (pubK_base64, privK_base64)

def armazena_chave(pem_content: tuple[str, str]) -> bool:
    public_pem = wrap_pem(pem_content[0], "RSA PUBLIC KEY")
    private_pem = wrap_pem(pem_content[1], "RSA PRIVATE KEY")
    try:
        with open("public_key.pem", "w") as f:
            f.write(public_pem)
        with open("private_key.pem", "w") as f:
            f.write(private_pem)
        return True    
    except:
        raise OSError("Erro ao criar arquivos")

def cria_key_string(key: tuple[int, int]) -> str:
    return f"modulo: {key[1]}\nexpoente: {key[0]}"

# Criar conteúdo PEM com quebras de linha a cada 64 caracteres
def wrap_pem(content_b64: str, tipo: str) -> str:
    linhas = [content_b64[i:i+64] for i in range(0, len(content_b64), 64)]
    return f"-----BEGIN {tipo}-----\n" + '\n'.join(linhas) + f"\n-----END {tipo}-----\n"