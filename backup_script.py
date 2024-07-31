import os
import mysql.connector
import boto3
import datetime
import gzip
import shutil

# Configuration from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAMES = os.getenv('DB_NAMES').split(',')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
SPACE_NAME = os.getenv('SPACE_NAME')
SPACE_REGION = os.getenv('SPACE_REGION')
SPACE_ENDPOINT = f'https://{SPACE_REGION}.digitaloceanspaces.com'


def backup_database(db_name):
    backup_file = f"backup_{db_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    command = f"mysqldump -h {DB_HOST} -P {DB_PORT} -u {DB_USER} -p{DB_PASSWORD} {db_name} > {backup_file}"
    os.system(command)
    return backup_file


def compress_file(file_path):
    compressed_file = f"{file_path}.gz"
    with open(file_path, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(file_path)  # Remove the original .sql file
    return compressed_file


def upload_to_digitalocean(file_path):
    s3_client = boto3.client(
        's3',
        endpoint_url=SPACE_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    with open(file_path, 'rb') as file:
        s3_client.upload_fileobj(file, SPACE_NAME, os.path.basename(file_path))
    print(f'{file_path} uploaded to DigitalOcean Spaces.')


if __name__ == "__main__":
    for db_name in DB_NAMES:
        backup_file = backup_database(db_name)
        compressed_file = compress_file(backup_file)
        upload_to_digitalocean(compressed_file)
        # Optional: remove the compressed file after upload
        os.remove(compressed_file)
