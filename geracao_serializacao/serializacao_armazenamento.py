import base64

from geracao_serializacao.geracao_chaves import geracao_chaves_rsa

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