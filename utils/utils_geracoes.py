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