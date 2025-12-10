# Implementação de Assinatura Digital com RSA-PSS

Este projeto apresenta uma implementação completa do esquema de assinatura digital RSA com o preenchimento PSS (Probabilistic Signature Scheme), desenvolvido em Python puro, sem o uso de bibliotecas criptográficas externas. O objetivo é demonstrar os conceitos fundamentais e os passos envolvidos no processo de assinatura e verificação de documentos digitais.

## Como Funciona

O fluxo de assinatura e verificação digital é implementado da seguinte maneira:

1.  **Geração de Chaves**:
    *   O sistema começa gerando dois números primos grandes (`p` e `q`) que são a base para o par de chaves RSA.
    *   Com base nesses primos, são calculados `n` (o módulo) e `phi(n)`.
    *   O expoente público `e` é definido (usando o valor comum 65537 por eficiência e segurança) e o expoente privado `d` é calculado.
    *   As chaves (pública e privada) são geradas e armazenadas em formato PEM para uso futuro.

2.  **Processo de Assinatura**:
    *   Uma mensagem (ou documento) é fornecida como entrada.
    *   Um hash criptográfico da mensagem é gerado usando o algoritmo `SHA3-256`.
    *   O esquema de preenchimento PSS é aplicado ao hash para adicionar aleatoriedade e aumentar a segurança contra ataques.
    *   O resultado (hash com preenchimento) é então cifrado com a **chave privada** RSA, resultando na assinatura digital.

3.  **Processo de Verificação**:
    *   Para verificar, o sistema recebe a mensagem original, a assinatura digital e a **chave pública**.
    *   O hash da mensagem original é recalculado.
    *   A assinatura é decifrada com a chave pública para recuperar o hash preenchido original.
    *   O preenchimento PSS é removido do hash recuperado.
    *   Finalmente, o hash recalculado e o hash extraído da assinatura são comparados. Se forem idênticos, a assinatura é considerada **válida**, garantindo a autenticidade e a integridade da mensagem.

## Estrutura do Projeto

O código está organizado de forma modular para separar as diferentes responsabilidades do processo:

```
/
├───.gitignore
├───main.py                         # Ponto de entrada e script de demonstração
├───assinatura_documento.py         # Orquestra o processo de assinatura
├───verifica_assinatura_documento.py # Orquestra o processo de verificação
├───cifracao_decifracao/            # Módulo de cifragem e decifragem RSA
│   ├───cifracao_rsapss.py
│   └───decifracao_rsapss.py
├───geracao_serializacao/           # Módulo para geração e armazenamento de chaves
│   ├───geracao_chaves.py
│   ├───geracao_primo.py
│   └───serializacao_armazenamento.py
├───pss/                             # Módulo de implementação do preenchimento PSS
│   └───pss_padding.py
├───utils/                           # Funções utilitárias
│   ├───utils_geracoes.py
│   └───utils_rsapss.py
└───verificacao/                     # Módulo principal da lógica de verificação
    └───verificar_assinatura.py
```

## Como Usar

Este projeto inclui um script principal (`main.py`) que demonstra todo o fluxo de assinatura e verificação.

Para executá-lo, basta rodar o seguinte comando no seu terminal:

```bash
python3 main.py
```

O script irá:
1.  Solicitar que você digite uma mensagem a ser assinada.
2.  Gerar um novo par de chaves RSA.
3.  Armazenar as chaves nos arquivos `public_key.pem` e `private_key.pem`.
4.  Assinar a mensagem que você forneceu.
5.  Verificar a assinatura gerada.
6.  Imprimir no console o resultado da verificação (se a assinatura é válida ou não).

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
