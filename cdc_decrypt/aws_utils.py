import boto3
import gzip
import json
from botocore.exceptions import ClientError
import re
import urllib.parse


def write_json_gz_to_s3(json_data, bucket_name, file_path, aws_access_key=None, aws_secret_key=None):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    compressed_data = gzip.compress(json.dumps(json_data).encode('utf-8'))
    s3.put_object(Body=compressed_data, Bucket=bucket_name, Key=file_path)



def read_json_from_s3(bucket_name, file_key, access_key=None, secret_key=None):
    # Create S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    # Download and read JSON file
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    json_data = response['Body'].read().decode('utf-8')
    data = json.loads(json_data)

    return data


def download_json_from_s3(bucket_name, file_key, destination_path, access_key=None, secret_key=None):

    # Create S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    # Download the JSON file from S3
    s3.download_file(bucket_name, file_key, destination_path)


def parse_filename(s3_key):
    ds_regex = r'ds=(\d{4}-\d{2}-\d{2})'
    ds_match = re.search(ds_regex, s3_key)
    ds = ds_match.group(1) if ds_match else None

    app_regex = r'\/([^/\.]+)\.'
    app_match = re.search(app_regex, s3_key)
    application = app_match.group(1) if app_match else None

    table_regex = r'\.([^./]+)\/'
    table_match = re.search(table_regex, s3_key)
    table = table_match.group(1) if table_match else None

    filename_match = re.search(r'([^\/]+)\.json\.gz$', s3_key)
    filename = filename_match.group(1) if filename_match else None

    return application, table, ds, filename



def get_s3_key(record):
    return urllib.parse.unquote(record['s3']['object']['key'])


def get_s3_key_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        record = data['Records'][0]  # Assumindo que há apenas um registro no arquivo
        return urllib.parse.unquote(record['s3']['object']['key'])



def get_secret(aws_access_key=None, aws_secret_key=None):

    secret_name = "SMB_KEY_TEST"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    client = boto3.client('secretsmanager',
                           region_name=region_name,
                           aws_access_key_id=aws_access_key,
                           aws_secret_access_key=aws_secret_key,
                           verify=False)

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated secret manager key
    secrets = get_secret_value_response['SecretString']

    secrets_dict = json.loads(secrets)

    key = secrets_dict['MYSQL_AES_KEY_SMB_FAKE']
    iv = secrets_dict['MYSQL_AES_IV_SMB_FAKE']

    return key, iv

key, iv = get_secret()
print(key, iv)