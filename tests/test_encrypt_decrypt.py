import hashlib
import json
from unittest import mock
from cdc_decrypt.cipher import convert_key_to_sha512, process_columns

def test_convert_key_to_sha512():
    # Cenário de teste 1: chave com 16 bytes
    key1 = "ticpebEoSH4sNs4PoGnhpyHHkXPoAdF3"
    result1 = convert_key_to_sha512(key1)
    assert len(result1) == 16

def test_process_columns():
    # Abre o arquivo JSON e carrega os dados
    with open('/Users/cora/Documents/cdc-decrypt/data/mock_data.json') as file:
        data_dict = json.load(file)

    columns = ["doing_business_as", "main_activity", "status"]

    # Simula a função de processamento
    def mock_process_func(cipher, value):
        assert isinstance(value, str)  # Verifica se o valor foi convertido em uma string
        return value

    # Chama a função process_columns
    result = process_columns(None, columns, data_dict, mock_process_func)



