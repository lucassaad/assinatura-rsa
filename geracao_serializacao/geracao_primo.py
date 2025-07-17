import random
from utils.utils_geracoes import nBitRandom


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