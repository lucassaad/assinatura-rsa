import random
from src.rsa_pss_signer.utils import nBitRandom
import base64



BITS_CHAVE = 1024

NUMBER_OF_RABIN_ROUNDS = 40


class PrimeGenerator():

    def __init__(self, first_primes_list: list[int]):
        self.first_primes_list = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67,
            71, 73, 79, 83, 89, 97, 101, 103,
            107, 109, 113, 127, 131, 137, 139,
            149, 151, 157, 163, 167, 173, 179,
            181, 191, 193, 197, 199, 211, 223,
            227, 229, 233, 239, 241, 251, 257,
            263, 269, 271, 277, 281, 283, 293,
        ]


    def _lowPrimes_primalityTest(self, num: int) -> bool:
        """
        Low-level primality test: trial division by small primes
        """
        for divisor in self.first_primes_list:
            if num % divisor == 0:
                return False
        return True     

    def _trialComposite(self, base:int, k: int, expoente: int, num: int) -> bool:
        """
        01. calculate a**m (mod num)
        02. if b0 == 1 or -1, num is probably prime
        03. else, for i from 1 to k - 1:
            3.1 calculate bi = bi-1**2 (mod num)
            3.2 if bi == 1, num is composite
            3.3 if bi == -1, num is probably prime
            obs: if bi == 1, num is composite, else if bi == -1, num is probably prime
        """
        result = pow(base, expoente, num)
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

    def _millerRabin_primalityTest(self, num: int) -> bool:
        """
        Miller-Rabin Primality Test:
        01. find 'k' and 'm' such that num - 1 = 2**k * m 
        02. for a number of rounds:
            2.1 choose a random 'a' in the range [2, num - 2]
            2.2 if trialComposite(a, k, m, num) returns True, then num is composite
        """

        k  = 0 # max division by two 
        m = num - 1 # even component

        while m % 2 == 0:
            m >>= 1 
            k += 1 

        # repeticao do processo de conclusao do miller rabin para garantir assertividade   
        for _ in range(NUMBER_OF_RABIN_ROUNDS):        
            a = random.randrange(2, num - 1)
            if (self._trialComposite(a, k, m, num)):
                return False
        return True   

    def geracao_num_primo(self, num_bits: int) -> int:
        """
        01. While prime not found:
            1.1 Generate a random n-bit odd number
            1.2 If lowLevelPrimalityTest(number) is True:
                1.2.1 If millerRabinPrimalityTest(number) is True:
        """
        while True:
            random_n_bit_number = nBitRandom(num_bits)
            lowLevelPrimality_result = self._lowPrimes_primalityTest(random_n_bit_number)
            if not lowLevelPrimality_result:
                continue
            prime_number_result = self._millerRabin_primalityTest(random_n_bit_number)
            if not prime_number_result: 
                continue

            return random_n_bit_number


# Primeiro teste de primalidade:
# dividir pelos primeiros numeros primos 
# importancia: elimina previamente numeros compostos faceis de reconhecer

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



