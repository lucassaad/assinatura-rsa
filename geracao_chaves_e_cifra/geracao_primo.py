import random


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
def geracao_num_primo(num_bits):
    while True:
        random_n_bit_number = nBitRandom(num_bits)
        lowLevelPrimality_result = lowPrimes_primalityTest(random_n_bit_number)
        if lowLevelPrimality_result:
            prime_number_result = millerRabin_primalityTest(random_n_bit_number)
            if prime_number_result: 
                return random_n_bit_number    
            
# objetivo: chave de 2048 bits.
# Para implementacao no projeto, escolheremos 2 numeros primos de 1024 bits.
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

# Primeiro teste de primalidade:
# dividir pelos primeiros numeros primos 
# importancia: elimina previamente numeros compostos faceis de reconhecer
def lowPrimes_primalityTest(num):
    for divisor in first_primes_list:
        if num % divisor == 0:
            return False
    return True     

# Miller Rabin
# teste deterministico para saber se um numero e primo ou não

def millerRabin_primalityTest(num):
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
        if not (trialComposite(a, k, m, num)):
            return False
    return True   
         
def trialComposite(a, k, m, num):
    # terceira etapa:
    # calcular b0 = a**m (mod num)
    # para b0: se b0 == 1 ou -1, num provavelmente primo
    # se b0 != 1 ou -1: calcular: b1 = b0**2 mod(num), e assim por diante
    # para b1,b2,..,bn: 1->composto, -1->primo 
        result = pow(a, m, num) # pow(base, expoente, modulo)
        if result == 1 or result == num - 1:
            return True
        else:
            for _ in range(k - 1):
                result = pow(result, 2, num)
                if result == 1:
                    return False
                elif result == num - 1:
                    return True
            return False    