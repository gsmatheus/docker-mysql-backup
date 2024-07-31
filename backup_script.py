import os
import mysql.connector
import boto3
import datetime

# Configurações a partir de variáveis de ambiente
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
SPACE_NAME = os.getenv('SPACE_NAME')
SPACE_REGION = os.getenv('SPACE_REGION')
SPACE_ENDPOINT = f'https://{SPACE_REGION}.digitaloceanspaces.com'

# Função para fazer backup do banco de dados


def backup_database():
    backup_file = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    command = f"mysqldump -h {DB_HOST} -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {backup_file}"
    os.system(command)
    return backup_file

# Função para enviar o backup para o DigitalOcean Spaces


def upload_to_digitalocean(file_path):
    s3_client = boto3.client(
        's3',
        endpoint_url=SPACE_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    with open(file_path, 'rb') as file:
        s3_client.upload_fileobj(file, SPACE_NAME, file_path)
    print(f'{file_path} enviado para o DigitalOcean Spaces.')


if __name__ == "__main__":
    backup_file = backup_database()
    upload_to_digitalocean(backup_file)
    # Opcional: excluir o arquivo após o envio
    os.remove(backup_file)
