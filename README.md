## Sobre o Algoritmo AES (Modo CBC)

O AES (Advanced Encryption Standard) é um algoritmo amplamente utilizado para criptografia. O modo CBC (Cipher Block Chaining) é um dos modos de operação que podem ser usados com o AES. Esse modo divide a mensagem em blocos e criptografa cada bloco individualmente, adicionando um bloco anterior para aumentar a segurança. O modo CBC usa um vetor de inicialização exclusivo para cada mensagem, garantindo a unicidade da saída criptografada. É um método popular para proteger dados confidenciais.

# Overview

Esse código define um conjunto de funções para criptografar e descriptografar valores JSON, usando o algoritmo AES (Advanced Encryption Standard). As funções envolvem a conversão de chaves, processamento de colunas, criptografia e descriptografia de valores, e o processamento de objetos JSON.

As funções `convert_key_to_sha512` converte a chave em um objeto sha512 e retorna os 16 primeiros bytes do hash, que é o comprimento necessário para a chave AES. 

A função `process_columns` processa um dicionário de dados `data_dict`, aplicando uma função de processamento `process_func` para cada valor em `data_dict` cuja chave está presente em uma lista de colunas `columns`.

As funções `encrypt_value` e `decrypt_value` criptografam e descriptografam valores usando AES com CBC (cipher-block chaining mode). O texto plano é preenchido com bytes de padding para o tamanho do bloco, em seguida, é criptografado e convertido em base64 para garantir que ele contenha apenas caracteres imprimíveis. 

A função `process_json` processa um objeto JSON `json_data`, aplicando a função `process_columns` para os valores do dicionário `after` (se ele estiver presente) e devolvendo o objeto JSON com os valores processados.

As funções `encrypt_json` e `decrypt_json` criptografam e descriptografam valores em um objeto JSON, respectivamente, aplicando as funções `process_json`, `encrypt_value` e `decrypt_value` nos valores que correspondem às colunas especificadas.

# Função `convert_key_to_sha512`
A função `convert_key_to_sha512` recebe uma chave como entrada e a converte em uma chave de 16 bytes usando o algoritmo SHA-512 (Secure Hash Algorithm 512 bits). 

Primeiro, a função codifica a chave fornecida em UTF-8 usando `key.encode('utf-8')`. Em seguida, ela calcula o hash SHA-512 dessa sequência de bytes usando `hashlib.sha512()`. O resultado é um objeto hash. 

Para obter a chave de 16 bytes, usamos `.digest()`, que retorna a representação binária do hash. Em seguida, utilizamos o fatiamento `[:16]` para obter somente os primeiros 16 bytes da chave. 

O valor retornado pela função é a chave convertida em SHA-512 de comprimento 16 bytes. Essa chave é geralmente usada como entrada para algoritmos de criptografia, como AES (Advanced Encryption Standard).

# Função `process_columns`
A função `process_columns` recebe um objeto `cipher`, uma lista de `columns` (colunas), um dicionário `data_dict` (dicionário de dados) e uma função `process_func` como parâmetros.

A função itera sobre os itens do dicionário `data_dict` usando o loop `for k, value in data_dict.items()`. Para cada item, verifica se a chave `k` está presente na lista de colunas `columns` usando a expressão `if k in columns`.

# Função `encrypt_value`
A função `encrypt_value` recebe um objeto `cipher` (cifra) e um valor `value` como parâmetros. A função realiza os seguintes passos:

1. O valor `value` é convertido em bytes usando `value.encode()` para obter sua representação em bytes.
2. O texto é preenchido (padding) para que tenha um tamanho múltiplo do tamanho do bloco AES usando a função `pad(value.encode(), AES.block_size)`.
3. O valor do texto preenchido é criptografado usando a cifra `cipher.encrypt(plain_text_padded)`.
4. O valor criptografado é codificado em base64 usando `base64.b64encode(encrypted_value)`.
5. O valor codificado em base64 é convertido em uma string usando `decode()` e é retornado como o valor criptografado.

# Função `decrypt_value`
A função `decrypt_value` recebe um objeto `decipher` (decifrador) e um valor criptografado `value` como parâmetros. A função realiza os seguintes passos:

1. O valor criptografado é decodificado da base64 para obter os bytes originais usando `base64.b64decode(value)`.
2. Os bytes decodificados são descriptografados usando o decifrador `decipher.decrypt(message_bytes)`.
3. O texto descriptografado é desempacotado (unpadding) para remover o preenchimento usando `unpad(decrypted_bytes, AES.block_size)`.
4. Os bytes desempacotados são decodificados em uma string usando `decode()`.
5. Se ocorrer um `ValueError` ou `TypeError` durante o processo de descriptografia, a função captura a exceção e retorna o valor original `value` em caso de erro.
6. Caso contrário, o valor descriptografado é retornado.

Em resumo, a função `encrypt_value` é responsável por criptografar um valor usando uma cifra AES e retornar o valor criptografado como uma string codificada em base64. A função `decrypt_value` faz o inverso, ou seja, decodifica um valor criptografado, descriptografa-o e retorna o valor original.

Se a chave estiver presente na lista de colunas, a função chama a função `process_func` passando o objeto `cipher` e o valor convertido em string usando `str(value)` como argumentos. O valor de retorno dessa chamada é atribuído à chave correspondente no dicionário `processed_dict`.

Se a chave não estiver presente na lista de colunas, o valor correspondente é simplesmente copiado para o dicionário `processed_dict`.

No final, a função retorna o dicionário `processed_dict`, que contém os valores processados de acordo com a lógica definida pela função `process_func` para as colunas especificadas.

# Função `process_json`
A função `process_json` realiza o processamento de um dicionário JSON (`json_data`) com base nos parâmetros fornecidos. Aqui está o que a função faz:

1. A chave `key` é convertida em uma chave de criptografia SHA-512 usando a função `convert_key_to_sha512(key)`. Isso garante que a chave seja adequada para ser usada como chave AES.
2. Um objeto `cipher` (cifra) AES é criado usando a chave SHA-512, o modo CBC e o vetor de inicialização (`iv`) fornecidos. O modo CBC (Cipher-Block Chaining) é um modo de operação de criptografia que adiciona aleatoriedade e torna a cifra mais segura. O vetor de inicialização (`iv`) é necessário para inicializar o processo de criptografia.
3. É criado um dicionário vazio `processed_dict` para armazenar os dados processados.
4. Um loop é percorrido em todos os itens do dicionário `json_data` usando o método `items()`. Cada item consiste em uma chave (`k`) e um valor (`value`).
5. Se a chave for igual a `'after'` e o valor for do tipo dicionário (`dict`), então o processamento de colunas é aplicado a esse valor chamando a função `process_columns`. Caso contrário, o valor é mantido inalterado.
6. O resultado do processamento é armazenado no dicionário `processed_dict` com a mesma chave (`k`).
7. Após o processamento de todos os itens do dicionário `json_data`, o dicionário `processed_dict` resultante é retornado.

Em resumo, a função `process_json` permite processar um dicionário JSON, aplicando uma função de processamento às colunas específicas do dicionário. O processamento envolve criptografar ou descriptografar os valores das colunas especificadas usando a cifra AES fornecida. O resultado é um novo dicionário com os valores processados.

# Funções `encrypt_json` e `decrypt_json`
Essas duas funções, `encrypt_json` e `decrypt_json`, são funções de conveniência para criptografar e descriptografar um dicionário JSON, respectivamente. Elas utilizam a função `process_json` para realizar o processamento, fornecendo a função apropriada de criptografia (`encrypt_value`) ou descriptografia (`decrypt_value`).

Aqui está uma descrição de cada função:

1. `encrypt_json(json_data, key, iv, columns_to_encrypt)`: Essa função recebe um dicionário JSON `json_data` e realiza a criptografia de colunas específicas (`columns_to_encrypt`). Ela utiliza a chave `key` e o vetor de inicialização (`iv`) fornecidos para configurar a cifra AES. A função `process_json` é chamada com os parâmetros adequados, incluindo a função de criptografia `encrypt_value`. O resultado é o dicionário JSON original com as colunas especificadas criptografadas.

2. `decrypt_json(json_data, key, iv, columns_to_decrypt)`: Essa função recebe um dicionário JSON `json_data` que foi criptografado anteriormente usando a função `encrypt_json`. Ela realiza a descriptografia das colunas específicas (`columns_to_decrypt`). Utiliza a chave `key` e o vetor de inicialização (`iv`) para configurar a cifra AES. A função `process_json` é chamada com os parâmetros adequados, incluindo a função de descriptografia `decrypt_value`. O resultado é o dicionário JSON original com as colunas especificadas descriptografadas.

Essas funções fornecem uma interface conveniente para criptografar e descriptografar um dicionário JSON, ocultando os detalhes de criptografia e descriptografia do código cliente. Isso simplifica o uso das funcionalidades de criptografia oferecidas pelas outras funções do código.