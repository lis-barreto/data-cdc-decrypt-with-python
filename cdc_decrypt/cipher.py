import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def convert_key_to_sha512(key):
    try:
        return hashlib.sha512(key.encode('utf-8')).digest()[:16]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def process_columns(cipher, columns, data_dict, process_func):
    processed_dict = {}
    for k, value in data_dict.items():
        if k in columns:
            processed_dict[k] = process_func(cipher, str(value))  # Convert value to string
        else:
            processed_dict[k] = value
    return processed_dict

def encrypt_value(cipher, value):
    plain_text_padded = pad(value.encode(), AES.block_size)
    encrypted_value = base64.b64encode(cipher.encrypt(plain_text_padded)).decode()
    return encrypted_value

def decrypt_value(decipher, value):
    try:
        message_bytes = base64.b64decode(value)
        decrypted_bytes = decipher.decrypt(message_bytes)
        decrypted_value = unpad(decrypted_bytes, AES.block_size).decode()
    except (ValueError, TypeError):
        decrypted_value = value
    return decrypted_value

def process_json(json_data, key, iv, columns_to_process, process_func):
    sha512_key = convert_key_to_sha512(key)
    cipher = AES.new(sha512_key, AES.MODE_CBC, iv.encode('utf-8'))
    processed_dict = {}
    for k, value in json_data.items():
        if k == 'after' and isinstance(value, dict):
            processed_dict[k] = process_columns(cipher, columns_to_process, value, process_func)
        else:
            processed_dict[k] = value
    return processed_dict

def encrypt_json(json_data, key, iv, columns_to_encrypt):
    return process_json(json_data, key, iv, columns_to_encrypt, encrypt_value)

def decrypt_json(json_data, key, iv, columns_to_decrypt):
    return process_json(json_data, key, iv, columns_to_decrypt, decrypt_value)
