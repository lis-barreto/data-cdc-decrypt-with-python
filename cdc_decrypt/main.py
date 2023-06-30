import json
import time
import pandas as pd
from cipher import encrypt_json, decrypt_json
from aws_utils import read_json_from_s3, get_secret

def main():
    start_time = time.time()

    # Read config file
    bucket_name = 'cora-data-stg-config'
    json_file = 'cdc_decrypt/refined/config/cora_apps/dumps_config.json'
    config = read_json_from_s3(bucket_name, json_file, access_key=None, secret_key=None)
    keys = ['application_name', 'original_table', 'encrypted_fields']
    result = [{key: d[key] for key in keys} for d in config]
    
    # Filter data from config file
    original_database = 'smb'
    original_table = 'business'
    filtered_config = []
    for item in result:
        if item.get("application_name") == original_database and item.get("original_table") == original_table:
            filtered_config.append(item)
    print(filtered_config)

    # Read JSON mock data from a file
    with open('./data/mock_data.json', 'r') as f:
        json_data = json.load(f)

    # Encrypt JSON data
    key, iv = get_secret()

    # Columns to encrypt
    columns_to_encrypt = []
    for item in filtered_config:
        if 'encrypted_fields' in item:
            columns_to_encrypt.extend(item['encrypted_fields'])
    print(columns_to_encrypt)

    bucket_name = 'cora-data-stg-custom'

    
    encrypted_data = encrypt_json(json_data, key, iv, columns_to_encrypt)

    file_name = "./data/data_encrypted.json"


    with open(file_name, "w") as json_file:
        json.dump(encrypted_data, json_file)

    print("Encrypted JSON data (local):")
    print(encrypted_data['after']['doing_business_as'])

    # Decrypt JSON data
    decrypted_data = decrypt_json(json_data, key, iv, columns_to_encrypt)
    print("Decrypted JSON data (local):")
    print(decrypted_data['after']['doing_business_as'])

    # Print execution time
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")

if __name__ == '__main__':
    main()