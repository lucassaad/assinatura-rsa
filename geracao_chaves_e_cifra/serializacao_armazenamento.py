import base64

from geracao_chaves import geracao_chaves_rsa

def serializa_chave(num_bits):
    # Pegar chaves
    keys = geracao_chaves_rsa(num_bits)
    # chave publica
    public_key = keys[0]
    pubK_str = cria_key_string(public_key)
    # chave privada
    private_key = keys[1]
    privK_str = cria_key_string(private_key)

    # str para bytes
    pubK_bytes = pubK_str.encode('ascii')
    privK_bytes = privK_str.encode('ascii')

    # bytes para base64
    pubK_base64 = base64.b64encode(pubK_bytes).decode('ascii')
    privK_base64 = base64.b64encode(privK_bytes).decode('ascii')
    
    # cria o conteudo para colocar no arquivo pem
    public_pem = wrap_pem(pubK_base64, "RSA PUBLIC KEY")
    private_pem = wrap_pem(privK_base64, "RSA PRIVATE KEY")
    
    return (public_pem, private_pem)

def armazena_chave(pem_content):
    with open("public_key.pem", "w") as f:
        f.write(pem_content[0])
    with open("private_key.pem", "w") as f:
        f.write(pem_content[1])

def cria_key_string(key):
    return f"modulo: {key[1]}\nexpoente: {key[0]}"

# Criar conteúdo PEM com quebras de linha a cada 64 caracteres
def wrap_pem(content_b64, tipo):
    linhas = [content_b64[i:i+64] for i in range(0, len(content_b64), 64)]
    return f"-----BEGIN {tipo}-----\n" + '\n'.join(linhas) + f"\n-----END {tipo}-----\n"